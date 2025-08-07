# Web Backend - FastAPI Service

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from fastapi import Body
from typing import List, Dict, Optional, Any
import hashlib
import secrets
import sqlite3
import json
from datetime import datetime, timedelta
import logging
import requests
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Titanic Web Backend", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Model Backend URL
MODEL_BACKEND_URL = os.getenv("MODEL_BACKEND_URL", "http://model-backend:5001")


# Data models
class UserRegistration(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: str
    is_admin: bool
    created_at: str


class PassengerData(BaseModel):
    pclass: int
    sex: str
    age: Optional[float]
    sibsp: int
    parch: int
    fare: float
    embarked: Optional[str]
    title: Optional[str]
    cabin_letter: Optional[str]


class PredictionRequest(BaseModel):
    passenger: PassengerData
    model_names: List[str]


class PredictionHistoryItem(BaseModel):
    id: int
    pclass: int
    sex: str
    age: int
    fare: float
    sibsp: int
    parch: int
    embarked: str
    title: str
    cabin_letter: str
    model_predictions: Dict[str, Any]
    created_at: str


class TrainModelRequest(BaseModel):
    model_name: str
    algorithm: str
    features: List[str]


# Database functions
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('titanic_app.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Prediction history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prediction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pclass INTEGER NOT NULL,
        sex TEXT NOT NULL,
        age INTEGER NOT NULL,
        fare REAL NOT NULL,
        sibsp INTEGER,
        parch INTEGER,
        embarked TEXT NOT NULL,
        title TEXT NOT NULL,
        cabin_letter TEXT NOT NULL,
        model_predictions TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create default admin user
    admin_password = hash_password("admin123")
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, is_admin)
        VALUES (?, ?, ?)
    ''', ("admin@titanic.com", admin_password, True))

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == password_hash


def create_session_token(user_id: int) -> str:
    """Create a new session token"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(days=7)

    conn = sqlite3.connect('titanic_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (token, user_id, expires_at)
        VALUES (?, ?, ?)
    ''', (token, user_id, expires_at))
    conn.commit()
    conn.close()

    return token


def get_user_from_token(token: str) -> Optional[Dict]:
    """Get user from session token"""
    conn = sqlite3.connect('titanic_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.id, u.email, u.is_admin, u.created_at
        FROM users u
        JOIN sessions s ON u.id = s.user_id
        WHERE s.token = ? AND s.expires_at > ?
    ''', (token, datetime.now()))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "id": result[0],
            "email": result[1],
            "is_admin": bool(result[2]),
            "created_at": result[3]
        }
    return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current authenticated user"""
    user = get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user


def get_admin_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """Get current user and verify admin privileges"""
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting Web Backend...")
    init_database()


@app.get("/")
async def root():
    return {"message": "Titanic Web Backend API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Authentication endpoints
@app.post("/api/auth/register")
async def register_user(user_data: UserRegistration):
    """Register a new user"""
    try:
        conn = sqlite3.connect('titanic_app.db')
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (user_data.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user
        password_hash = hash_password(user_data.password)
        cursor.execute('''
            INSERT INTO users (email, password_hash, is_admin)
            VALUES (?, ?, ?)
        ''', (user_data.email, password_hash, False))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Create session token
        token = create_session_token(user_id)

        return {
            "message": "User registered successfully",
            "token": token,
            "user": {
                "id": user_id,
                "email": user_data.email,
                "is_admin": False
            }
        }

    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/login")
async def login_user(user_data: UserLogin):
    """Login user"""
    try:
        conn = sqlite3.connect('titanic_app.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, email, password_hash, is_admin
            FROM users WHERE email = ?
        ''', (user_data.email,))

        result = cursor.fetchone()
        conn.close()

        if not result or not verify_password(user_data.password, result[2]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_id, email, _, is_admin = result

        # Create session token
        token = create_session_token(user_id)

        return {
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user_id,
                "email": email,
                "is_admin": bool(is_admin)
            }
        }

    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/logout")
async def logout_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user"""
    try:
        conn = sqlite3.connect('titanic_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE token = ?', (credentials.credentials,))
        conn.commit()
        conn.close()

        return {"message": "Logout successful"}

    except Exception as e:
        logger.error(f"Error logging out user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/auth/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    return {"user": current_user}


# Model management endpoints
@app.get("/api/models")
async def get_models(custom_only: bool = False, default_only: bool = False):
    """Get list of available models from Model Backend"""
    try:
        # Get the base URL
        base_url = f"{MODEL_BACKEND_URL}/api/models"

        # Add query parameters only if they're explicitly set to True
        # This ensures backward compatibility with the existing frontend
        params = {}
        if custom_only:
            params["custom_only"] = "true"
        if default_only:
            params["default_only"] = "true"

        # Make the request with parameters
        if params:
            response = requests.get(base_url, params=params)
        else:
            # Normal request without parameters - this should get ALL models
            response = requests.get(base_url)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(status_code=500, detail="Error fetching models")


@app.delete("/api/models/{model_id}")
async def delete_model(model_id: str, admin_user: Dict = Depends(get_admin_user)):
    """Delete a model (admin only)"""
    try:
        response = requests.delete(f"{MODEL_BACKEND_URL}/api/models/{model_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error deleting model: {e}")
        raise HTTPException(status_code=500, detail="Error deleting model")


@app.post("/api/models/train")
async def train_model(request: TrainModelRequest, admin_user: Dict = Depends(get_admin_user)):
    """Train a new model (admin only)"""
    try:
        response = requests.post(f"{MODEL_BACKEND_URL}/api/train", json=request.model_dump())
        response.raise_for_status()
        return response.json()

    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail="Error training model")


@app.get("/api/features")
async def get_features():
    """Get available features for training"""
    try:
        response = requests.get(f"{MODEL_BACKEND_URL}/api/features")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching features: {e}")
        raise HTTPException(status_code=500, detail="Error fetching features")


def get_current_user_or_none(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Get current user if authenticated, otherwise return None"""
    if credentials is None:
        return None

    try:
        user = get_user_from_token(credentials.credentials)
        return user
    except Exception:
        return None


@app.post("/api/predict")
async def predict_survival(
        request: PredictionRequest = Body(...),
        current_user: Optional[Dict] = Depends(get_current_user_or_none)
):
    """Make survival prediction"""
    try:
        # For anonymous users, restrict to RF and SVM models only
        if not current_user:
            # Get available models to check which are RF/SVM
            try:
                models_response = requests.get(f"{MODEL_BACKEND_URL}/api/models")
                if models_response.status_code == 200:
                    models = models_response.json()

                    # Extract algorithms for each model
                    model_algorithms = {}
                    for model in models:
                        name = model.get("name")
                        algorithm = model.get("algorithm")
                        if name and algorithm:
                            model_algorithms[name.lower()] = algorithm

                    # Check if ANY requested model is not allowed
                    for model_name in request.model_names:
                        # Case insensitive comparison
                        algorithm = model_algorithms.get(model_name.lower())
                        if not algorithm or algorithm not in ["random_forest", "svm"]:
                            logger.warning(f"Anonymous user tried to use restricted model: {model_name}")
                            raise HTTPException(
                                status_code=403,
                                detail="Anonymous users can only use Random Forest and SVM models."
                            )
            except Exception as e:
                # Just log and continue if we can't check - don't block legitimate requests
                logger.warning(f"Couldn't verify model restrictions: {str(e)}")

        # Ensure passenger data is properly formatted
        passenger_data = {
            "pclass": request.passenger.pclass,
            "sex": request.passenger.sex,
            "age": request.passenger.age if request.passenger.age is not None else 30,
            "sibsp": request.passenger.sibsp,
            "parch": request.passenger.parch,
            "fare": request.passenger.fare,
            "embarked": request.passenger.embarked or "S",
            "title": request.passenger.title or "Mr",
            "cabin_letter": request.passenger.cabin_letter or "U"
        }

        # Send data to model backend
        logger.info(f"Sending prediction request with data: {passenger_data}")

        response = requests.post(f"{MODEL_BACKEND_URL}/api/predict", json={
            "passenger": passenger_data,
            "model_names": request.model_names
        })

        response.raise_for_status()
        predictions = response.json()

        # Save to history if user is logged in
        if current_user:
            try:
                conn = sqlite3.connect('titanic_app.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO prediction_history 
                    (user_id, pclass, sex, age, fare, sibsp, parch, embarked, title, cabin_letter, model_predictions)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    current_user["id"],
                    request.passenger.pclass,
                    request.passenger.sex,
                    request.passenger.age or 30,
                    request.passenger.fare,
                    request.passenger.sibsp,
                    request.passenger.parch,
                    request.passenger.embarked or "S",
                    request.passenger.title or "Mr",
                    request.passenger.cabin_letter or "U",
                    json.dumps(predictions["predictions"])
                ))

                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving prediction history: {e}")

        return predictions

    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")


# Prediction history endpoints
@app.get("/api/history", response_model=List[PredictionHistoryItem])
async def get_prediction_history(current_user: Dict = Depends(get_current_user)):
    """Get user's prediction history (last 10)"""
    try:
        conn = sqlite3.connect('titanic_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, pclass, sex, age, fare, sibsp, parch, embarked, title, cabin_letter, model_predictions, created_at
            FROM prediction_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        ''', (current_user["id"],))

        results = cursor.fetchall()
        conn.close()

        history = []
        for result in results:
            history.append(PredictionHistoryItem(
                id=result[0],
                pclass=result[1],
                sex=result[2],
                age=result[3],
                fare=result[4],
                sibsp=result[5],
                parch=result[6],
                embarked=result[7],
                title=result[8],
                cabin_letter=result[9],
                model_predictions=json.loads(result[10]),
                created_at=result[11]
            ))

        return history

    except Exception as e:
        logger.error(f"Error fetching prediction history: {e}")
        raise HTTPException(status_code=500, detail="Error fetching prediction history")


# User management endpoints (admin only)
@app.get("/api/users")
async def get_users(admin_user: Dict = Depends(get_admin_user)):
    """Get list of all users (admin only)"""
    try:
        conn = sqlite3.connect('titanic_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, is_admin, created_at FROM users')
        results = cursor.fetchall()
        conn.close()

        users = []
        for result in results:
            users.append({
                "id": result[0],
                "email": result[1],
                "is_admin": bool(result[2]),
                "created_at": result[3]
            })

        return users

    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users")


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, admin_user: Dict = Depends(get_admin_user)):
    """Delete a user (admin only)"""
    try:
        if user_id == admin_user["id"]:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")

        conn = sqlite3.connect('titanic_app.db')
        cursor = conn.cursor()

        # Delete user's sessions and history
        cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM prediction_history WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        conn.commit()
        conn.close()

        return {"message": "User deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Error deleting user")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)