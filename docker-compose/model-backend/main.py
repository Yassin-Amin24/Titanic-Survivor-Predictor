from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, Perceptron, SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Titanic Model Backend", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class PassengerData(BaseModel):
    pclass: Optional[int] = None
    sex: Optional[str] = None
    age: Optional[float] = None
    sibsp: Optional[int] = None
    parch: Optional[int] = None
    fare: Optional[float] = None
    embarked: Optional[str] = None
    title: Optional[str] = None
    cabin_letter: Optional[str] = None


class PredictionRequest(BaseModel):
    passenger: PassengerData
    model_names: List[str]


class PredictionResponse(BaseModel):
    predictions: Dict[str, Dict[str, Any]]  # model_name -> {prediction, probability}


class TrainModelRequest(BaseModel):
    model_name: str
    algorithm: str  # "random_forest", "decision_tree", "knn", "svm", "logistic_regression", etc.
    features: List[str]


class ModelInfo(BaseModel):
    id: str
    name: str
    algorithm: str
    features: List[str]
    accuracy: float
    created_at: str
    is_default: bool


class PassengerFeatures(BaseModel):
    Pclass: Optional[int]
    Sex: Optional[str]
    Age: Optional[float]
    SibSp: Optional[int]
    Parch: Optional[int]
    Fare: Optional[float]
    Embarked: Optional[str]
    Title: Optional[str]
    CabinLetter: Optional[str]


# Global variables
models = {}
model_metadata = {}
train_df = None
test_df = None
combined_data = None
feature_encoders = {}
trained_model_features = {}
model_accuracy = {}

# Default algorithms mapping
ALGORITHMS = {
    "random_forest": RandomForestClassifier,
    "decision_tree": DecisionTreeClassifier,
    "knn": KNeighborsClassifier,
    "svm": SVC,
    "logistic_regression": LogisticRegression,
    "perceptron": Perceptron,
    "sgd": SGDClassifier,
    "gaussian_nb": GaussianNB
}


def load_dataset():
    """Load and preprocess the Titanic dataset following notebook approach"""
    global train_df, test_df, combined_data, feature_encoders

    try:
        # Load the datasets
        train_df = pd.read_csv("data/train.csv")
        test_df = pd.read_csv("data/test.csv")

        # Store original indices
        train_df['original_index'] = train_df.index
        test_df['original_index'] = test_df.index

        # Combine datasets for preprocessing
        test_df['Survived'] = np.nan  # Add target column to test for combining
        combined_data = pd.concat([train_df, test_df], sort=False).reset_index(drop=True)

        # Feature engineering based on the notebook approach

        # Extract titles from names
        combined_data['Title'] = combined_data['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

        # Map titles to standardized categories
        title_mapping = {
            'Mr': 'Mr',
            'Miss': 'Miss',
            'Mrs': 'Mrs',
            'Master': 'Master',
            'Dr': 'Rare',
            'Rev': 'Rare',
            'Col': 'Rare',
            'Major': 'Rare',
            'Mlle': 'Miss',
            'Mme': 'Mrs',
            'Ms': 'Miss',
            'Lady': 'Rare',
            'Sir': 'Rare',
            'Capt': 'Rare',
            'the Countess': 'Rare',
            'Jonkheer': 'Rare',
            'Don': 'Rare'
        }
        combined_data['Title'] = combined_data['Title'].map(lambda x: title_mapping.get(x, 'Rare'))

        # Create family size feature
        combined_data['FamilySize'] = combined_data['SibSp'] + combined_data['Parch'] + 1

        # Create IsAlone feature
        combined_data['IsAlone'] = (combined_data['FamilySize'] == 1).astype(int)

        # Calculate median ages by title - FIXED APPROACH
        title_age_medians = combined_data.groupby('Title')['Age'].median().to_dict()

        # Fill missing ages using title medians
        for title, median_age in title_age_medians.items():
            combined_data.loc[(combined_data['Age'].isnull()) & (combined_data['Title'] == title), 'Age'] = median_age

        # Fill any remaining NaN with overall median
        overall_age_median = combined_data['Age'].median()
        combined_data['Age'].fillna(overall_age_median, inplace=True)

        # Create Age bins and convert to ordinal
        # First create the Age bands
        combined_data['AgeBand'] = pd.cut(combined_data['Age'], 5)
        # Then convert to numerical code
        combined_data['AgeBin'] = combined_data['AgeBand'].cat.codes

        # Create Age_Class interaction
        combined_data['Age_Class'] = combined_data['Age'] * combined_data['Pclass']

        # Process Embarked - fill missing values with most common
        combined_data['Embarked'].fillna(combined_data['Embarked'].mode()[0], inplace=True)

        # Process Fare - fill missing values with median by Pclass
        for pclass in [1, 2, 3]:
            pclass_fare_median = combined_data.loc[combined_data['Pclass'] == pclass, 'Fare'].median()
            combined_data.loc[
                (combined_data['Fare'].isnull()) & (combined_data['Pclass'] == pclass), 'Fare'] = pclass_fare_median

        # Create Fare bands and convert to ordinal
        combined_data['FareBand'] = pd.qcut(combined_data['Fare'], 4)
        combined_data['FareBin'] = combined_data['FareBand'].cat.codes

        # Create family size categories
        combined_data['FamilySizeGroup'] = pd.cut(combined_data['FamilySize'],
                                               bins=[0, 1, 4, 7, 11],
                                               labels=['Single', 'Small', 'Medium', 'Large'])
        combined_data['FamilySizeBin'] = combined_data['FamilySizeGroup'].cat.codes

        # Extract cabin letter (deck) from cabin
        combined_data['CabinLetter'] = combined_data['Cabin'].astype(str).str[0]
        combined_data.loc[combined_data['CabinLetter'] == 'n', 'CabinLetter'] = 'U'  # 'n' from 'nan' -> 'U' for unknown

        # Encode categorical variables
        le_sex = LabelEncoder()
        le_embarked = LabelEncoder()
        le_title = LabelEncoder()
        le_cabin = LabelEncoder()

        combined_data['Sex_encoded'] = le_sex.fit_transform(combined_data['Sex'])
        combined_data['Embarked_encoded'] = le_embarked.fit_transform(combined_data['Embarked'])
        combined_data['Title_encoded'] = le_title.fit_transform(combined_data['Title'])
        combined_data['Cabin_encoded'] = le_cabin.fit_transform(combined_data['CabinLetter'])

        # Store encoders
        feature_encoders = {
            'sex': le_sex,
            'embarked': le_embarked,
            'title': le_title,
            'cabin': le_cabin
        }

        # Re-split the combined data back to train and test
        train_df = combined_data.loc[combined_data['Survived'].notna()].copy()
        test_df = combined_data.loc[combined_data['Survived'].isna()].copy()

        logger.info(f"Datasets loaded and processed: Train: {len(train_df)} records, Test: {len(test_df)} records")
        return train_df, test_df, combined_data

    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise



def preprocess_passenger_data(passenger: PassengerData) -> pd.DataFrame:
    """Convert passenger input to features dataframe with proper feature names"""
    data = passenger.model_dump()

    # Provide default values if any are missing or None
    data["Pclass"] = data.get("pclass") or 3
    data["Sex"] = data.get("sex") or "male"
    data["Age"] = data.get("age") if data.get("age") is not None else 30
    data["SibSp"] = data.get("sibsp") if data.get("sibsp") is not None else 0
    data["Parch"] = data.get("parch") if data.get("parch") is not None else 0
    data["Fare"] = data.get("fare") if data.get("fare") is not None else 32.2
    data["Embarked"] = data.get("embarked") or "S"
    data["Title"] = data.get("title") or "Mr"

    # Derived features
    data["Age_Class"] = data["Age"] * data["Pclass"]

    # Encodings
    data["Sex_encoded"] = 0 if data["Sex"] == "male" else 1
    data["Embarked_encoded"] = {"S": 0, "C": 1, "Q": 2}.get(data["Embarked"], 0)
    data["Title_encoded"] = {
        "Mr": 0, "Miss": 1, "Mrs": 2, "Master": 3, "Rare": 4
    }.get(data["Title"], 0)

    # Create feature dictionary with core features that all models use
    feature_dict = {
        'Pclass': data["Pclass"],
        'Sex_encoded': data["Sex_encoded"],
        'Age': data["Age"],
        'SibSp': data["SibSp"],
        'Parch': data["Parch"],
        'Fare': data["Fare"],
        'Embarked_encoded': data["Embarked_encoded"],
        'Title_encoded': data["Title_encoded"],
    }

    return pd.DataFrame([feature_dict])


def train_default_models():
    """Train all default models on startup using notebook approach"""
    global models, model_metadata, train_df, test_df

    if train_df is None:
        load_dataset()

    train_df['Age_Class'] = train_df['Age'] * train_df['Pclass']
    train_df['Age*Class'] = train_df['Age'] * train_df['Pclass']

    # Define feature columns based on the notebook
    # feature_columns = [
    #     'Pclass', 'Sex_encoded', 'Age', 'SibSp', 'Parch', 'Fare',
    #     'Embarked_encoded', 'Title_encoded', 'FamilySize',
    #     'IsAlone', 'Age_Class', 'Cabin_encoded',
    #     'AgeBin', 'FareBin', 'FamilySizeBin'
    # ]


    core_features = [
        'Pclass', 'Sex_encoded', 'Age', 'SibSp', 'Parch', 'Fare',
        'Embarked_encoded', 'Title_encoded'
    ]

    X = train_df[core_features]
    y = train_df['Survived']

    # Feature scaling for better performance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Store the scaler for future use
    os.makedirs("models", exist_ok=True)

    # Clear existing default models (to prevent accumulation)
    for f in os.listdir("models"):
        if f.startswith("default_") and os.path.isfile(os.path.join("models", f)):
            os.remove(os.path.join("models", f))

        # Clean up global dictionaries
    for model_id in list(models.keys()):
        if model_id.startswith("default_"):
            if model_id in models:
                del models[model_id]
            if model_id in model_metadata:
                del model_metadata[model_id]
            if model_id in trained_model_features:
                del trained_model_features[model_id]

    # Define cross-validation
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    # Train each algorithm
    for algo_name, algo_class in ALGORITHMS.items():
        try:
            logger.info(f"Training {algo_name} model...")

            # Configure algorithm parameters based on notebook
            if algo_name == "random_forest":
                model = algo_class(n_estimators=100, criterion="gini",
                                   max_depth=5,
                                   min_samples_split=10, min_samples_leaf=1,
                                   max_features='sqrt', random_state=42)
            elif algo_name == "decision_tree":
                model = algo_class(criterion="gini", max_depth=5, min_samples_split=10, random_state=42)
            elif algo_name == "knn":
                model = algo_class(n_neighbors=5, weights="uniform", algorithm="auto", p=2)  # Use 5 neighbors
            elif algo_name == "svm":
                model = algo_class(kernel="linear", C=0.025, probability=True, random_state=42)  # Use linear kernel
            elif algo_name == "logistic_regression":
                model = algo_class(penalty="l2", C=0.1, solver="lbfgs", max_iter=1000, random_state=42)
            elif algo_name == "perceptron":
                model = algo_class(penalty="l2", alpha=0.0001, max_iter=1000, tol=1e-3, random_state=42)
            elif algo_name == "sgd":
                model = algo_class(loss="modified_huber", penalty="l2", max_iter=1000, tol=1e-3, random_state=42)
            elif algo_name == "gaussian_nb":
                model = algo_class()
            else:
                model = algo_class(random_state=42 if hasattr(algo_class, "random_state") else None)

            # Cross validation
            cv_scores = cross_val_score(model, X_scaled, y, cv=kfold, scoring="accuracy")
            cv_mean = np.mean(cv_scores)

            # Train final model on full training data
            model.fit(X_train, y_train)

            # Calculate accuracy on test set
            y_pred = model.predict(X_test)
            test_accuracy = accuracy_score(y_test, y_pred)

            # Store model
            model_id = f"default_{algo_name}"
            models[model_id] = model
            trained_model_features[model_id] = core_features
            model_accuracy[model_id] = round(test_accuracy, 4)
            model_metadata[model_id] = {
                "id": model_id,
                "name": algo_name.replace("_", " ").title(),
                "algorithm": algo_name,
                "features": core_features,
                "accuracy": round(test_accuracy, 4),
                "cv_accuracy": round(cv_mean, 4),
                "created_at": datetime.now().isoformat(),
                "is_default": True
            }


            # Save model to disk
            model_path = f"models/{model_id}.pkl"
            # features_path = f"models/{model_id}_features.pkl"
            # metadata_path = f"models/{model_id}_metadata.pkl"

            joblib.dump(model, model_path)

            # with open(features_path, "wb") as f:
            #     pickle.dump(feature_columns, f)
            #
            # with open(metadata_path, "wb") as f:
            #     pickle.dump(model_metadata, f)

            logger.info(f"Trained {algo_name} with accuracy: {test_accuracy:.4f}, CV accuracy: {cv_mean:.4f}")

        except Exception as e:
            logger.error(f"Error training {algo_name}: {e}")



@app.on_event("startup")
async def startup_event():
    """Initialize models on startup - training default models fresh each time"""
    global models, model_metadata, trained_model_features

    logger.info("Starting Model Backend...")

    # Always train default models fresh at startup
    train_default_models()

    # Load any custom models
    if os.path.exists("models"):
        for model_file in os.listdir("models"):
            if model_file.endswith(".pkl") and not model_file.endswith("_scaler.pkl") and not model_file.endswith(
                    "_features.pkl"):
                model_id = model_file.replace(".pkl", "")

                # Skip default models as we just trained them
                if model_id.startswith("default_"):
                    continue

                try:
                    model = joblib.load(f"models/{model_file}")
                    models[model_id] = model

                    # Load associated features
                    features_path = f"models/{model_id}_features.pkl"
                    if os.path.exists(features_path):
                        with open(features_path, "rb") as f:
                            trained_model_features[model_id] = pickle.load(f)
                        logger.info(f"Loaded custom model: {model_id}")
                    else:
                        logger.warning(f"No feature list found for {model_id}; using fallback")
                        trained_model_features[model_id] = [
                            'Pclass', 'Sex_encoded', 'Age', 'Fare',
                            'Embarked_encoded', 'Title_encoded'
                        ]

                    # Create metadata for custom model
                    if model_id not in model_metadata:
                        model_metadata[model_id] = {
                            "id": model_id,
                            "name": model_id.replace("custom_", "").replace("_", " ").title(),
                            "algorithm": model_id.split("_")[1] if len(model_id.split("_")) > 1 else "unknown",
                            "features": trained_model_features[model_id],
                            "accuracy": model_accuracy[model_id],  # Default
                            "created_at": datetime.now().isoformat(),
                            "is_default": False
                        }

                except Exception as e:
                    logger.error(f"Error loading custom model {model_id}: {e}")


@app.get("/")
async def root():
    return {"message": "Titanic Model Backend API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": len(models)}


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make survival predictions using specified models"""
    try:
        if train_df is None:
            load_dataset()

        logger.info(f"Received prediction request for models: {request.model_names}")

        # Preprocess passenger data to standard format
        passenger_features = preprocess_passenger_data(request.passenger)
        logger.info(f"Processed passenger features: {list(passenger_features.columns)}")

        predictions = {}

        for model_name in request.model_names:
            try:
                # Find the model by name or ID
                model_id = None
                for mid, metadata in model_metadata.items():
                    if model_name.lower() == metadata["name"].lower() or model_name == mid:
                        model_id = mid
                        break

                if not model_id or model_id not in models:
                    logger.warning(f"Model not found: {model_name}")
                    predictions[model_name] = {
                        "prediction": "Error",
                        "error": f"Model '{model_name}' not found"
                    }
                    continue

                model = models[model_id]

                # Get the exact features this model was trained on
                model_features = trained_model_features.get(model_id)
                if not model_features:
                    logger.warning(f"No feature list for model {model_id}, using basic features")
                    model_features = ['Pclass', 'Sex_encoded', 'Age', 'Fare', 'Embarked_encoded', 'Title_encoded']

                # Extract only the features this model was trained on
                available_features = [f for f in model_features if f in passenger_features.columns]
                if len(available_features) < len(model_features):
                    logger.warning(f"Missing features for {model_id}: {set(model_features) - set(available_features)}")

                if len(available_features) < 3:
                    logger.error(f"Not enough features available for {model_id}")
                    predictions[model_name] = {
                        "prediction": "Error",
                        "error": "Not enough features available"
                    }
                    continue

                # Create a new dataframe with only the needed features, without feature names
                # This prevents the sklearn warning about feature names
                X = passenger_features[available_features].values

                # Make prediction
                prediction = int(model.predict(X)[0])

                # Get probability if available
                probability = None
                if hasattr(model, "predict_proba"):
                    try:
                        proba = model.predict_proba(X)[0]
                        probability = {
                            "survived": float(proba[1]),
                            "died": float(proba[0])
                        }
                    except Exception as e:
                        logger.warning(f"Could not get probability for {model_name}: {e}")

                # Store prediction result
                predictions[model_name] = {
                    "prediction": "Survived" if prediction == 1 else "Did not survive",
                    "prediction_value": prediction,
                    "probability": probability
                }

                logger.info(f"Successful prediction with {model_name}: {prediction}")

            except Exception as e:
                logger.error(f"Error predicting with {model_name}: {e}")
                predictions[model_name] = {
                    "prediction": "Error",
                    "error": str(e)
                }

        return PredictionResponse(predictions=predictions)

    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models", response_model=List[ModelInfo])
async def get_models(custom_only: bool = False, default_only: bool = False):
    """Get list of all available models with optional filtering"""
    if custom_only:
        result = [metadata for model_id, metadata in model_metadata.items() if not metadata["is_default"]]
    elif default_only:
        result = [metadata for model_id, metadata in model_metadata.items() if metadata["is_default"]]
    else:
        # Default behavior: return all models
        result = list(model_metadata.values())

    return result

@app.get("/api/models/default", response_model=List[ModelInfo])
async def get_default_models():
    """Get list of default models only"""
    default_models = [metadata for model_id, metadata in model_metadata.items() if metadata["is_default"]]
    return default_models

@app.get("/api/models/custom", response_model=List[ModelInfo])
async def get_custom_models():
    """Get list of custom models only"""
    custom_models = [metadata for model_id, metadata in model_metadata.items() if not metadata["is_default"]]
    return custom_models


@app.get("/api/features")
async def get_features():
    """Get list of available features for training"""
    if train_df is None:
        load_dataset()

    features = [
        {"name": "Pclass", "description": "Passenger class (1st, 2nd, 3rd)"},
        {"name": "Sex", "description": "Gender (Male, Female)"},
        {"name": "Age", "description": "Age in years"},
        {"name": "SibSp", "description": "Number of siblings/spouses aboard"},
        {"name": "Parch", "description": "Number of parents/children aboard"},
        {"name": "Fare", "description": "Ticket fare"},
        {"name": "Embarked", "description": "Port of embarkation"},
        {"name": "Title", "description": "Title extracted from name"},
        {"name": "FamilySize", "description": "Total family members aboard including passenger"},
        {"name": "IsAlone", "description": "Whether passenger traveled alone"},
        {"name": "Age_Class", "description": "Age * Class interaction"},
        {"name": "CabinLetter", "description": "Deck information from cabin"}
    ]

    return {"features": features}


@app.post("/api/train")
async def train_model(request: TrainModelRequest):
    """Train a new model with specified features and algorithm"""
    try:
        if train_df is None:
            load_dataset()

        if request.algorithm not in ALGORITHMS:
            raise HTTPException(status_code=400, detail=f"Algorithm '{request.algorithm}' not supported")

        # Map feature names to dataset columns
        feature_mapping = {
            "Pclass": "Pclass",
            "Sex": "Sex_encoded",
            "Age": "Age",
            "SibSp": "SibSp",
            "Parch": "Parch",
            "Fare": "Fare",
            "Embarked": "Embarked_encoded",
            "Title": "Title_encoded",
            "FamilySize": "FamilySize",
            "IsAlone": "IsAlone",
            "Age_Class": "Age_Class",
            "CabinLetter": "Cabin_encoded",
            "AgeBin": "AgeBin",
            "FareBin": "FareBin",
            "FamilySizeBin": "FamilySizeBin"
        }

        feature_columns = [feature_mapping[f] for f in request.features if f in feature_mapping]

        if not feature_columns:
            raise HTTPException(status_code=400, detail="No valid features specified")

        X = train_df[feature_columns]
        y = train_df['Survived']

        # Feature scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Define cross-validation
        kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

        # Create and train model
        algo_class = ALGORITHMS[request.algorithm]
        if request.algorithm == "random_forest":
            model = algo_class(n_estimators=100, criterion="gini", max_depth=None, min_samples_split=2,
                               min_samples_leaf=1, random_state=42)
        elif request.algorithm == "decision_tree":
            model = algo_class(criterion="gini", max_depth=None, random_state=42)
        elif request.algorithm == "svm":
            model = algo_class(kernel="rbf", gamma="auto", C=1.0, probability=True, random_state=42)
        elif request.algorithm == "knn":
            model = algo_class(n_neighbors=3, weights="uniform", algorithm="auto", p=2)
        elif request.algorithm == "logistic_regression":
            model = algo_class(penalty="l2", solver="lbfgs", max_iter=1000, random_state=42)
        elif request.algorithm == "perceptron":
            model = algo_class(penalty="l2", alpha=0.0001, max_iter=1000, tol=1e-3, random_state=42)
        elif request.algorithm == "sgd":
            model = algo_class(loss="modified_huber", penalty="l2", max_iter=1000, tol=1e-3, random_state=42)
        elif request.algorithm == "gaussian_nb":
            model = algo_class()
        else:
            model = algo_class(random_state=42 if hasattr(algo_class, "random_state") else None)

        # Cross validation
        cv_scores = cross_val_score(model, X_scaled, y, cv=kfold, scoring="accuracy")
        cv_mean = np.mean(cv_scores)

        # Train final model
        model.fit(X_train, y_train)

        # Calculate accuracy
        y_pred = model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)

        # Generate unique model ID
        model_id = f"custom_{request.model_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Store model
        models[model_id] = model
        trained_model_features[model_id] = feature_columns
        model_metadata[model_id] = {
            "id": model_id,
            "name": request.model_name,
            "algorithm": request.algorithm,
            "features": request.features,
            "accuracy": round(test_accuracy, 4),
            "cv_accuracy": round(cv_mean, 4),
            "created_at": datetime.now().isoformat(),
            "is_default": False
        }

        # Save model and scaler to disk
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, f"models/{model_id}.pkl")
        joblib.dump(scaler, f"models/{model_id}_scaler.pkl")
        with open(f"models/{model_id}_features.pkl", "wb") as f:
            pickle.dump(feature_columns, f)

        return {
            "message": f"Model '{request.model_name}' trained successfully",
            "model_id": model_id,
            "accuracy": test_accuracy,
            "cv_accuracy": cv_mean,
            "features_used": request.features
        }

    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/models/{model_id}")
async def delete_model(model_id: str):
    """Delete a trained model"""
    try:
        if model_id not in models:
            raise HTTPException(status_code=404, detail="Model not found")

        # Don't allow deletion of default models
        if model_metadata[model_id]["is_default"]:
            raise HTTPException(status_code=400, detail="Cannot delete default models")

        # Remove from memory
        del models[model_id]
        del model_metadata[model_id]

        # Remove from disk
        model_path = f"models/{model_id}.pkl"
        scaler_path = f"models/{model_id}_scaler.pkl"

        if os.path.exists(model_path):
            os.remove(model_path)

        if os.path.exists(scaler_path):
            os.remove(scaler_path)

        return {"message": f"Model '{model_id}' deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models/{model_id}")
async def get_model_details(model_id: str):
    """Get details of a specific model"""
    if model_id not in model_metadata:
        raise HTTPException(status_code=404, detail="Model not found")

    return model_metadata[model_id]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)