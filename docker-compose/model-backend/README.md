# Model Backend – Titanic Survival Prediction

This backend service provides a REST API for machine learning model training and inference. It supports multiple classification algorithms for predicting Titanic passenger survival.

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd model-backend
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Run the Application

### Option 1: Run with Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Option 2: Run with Docker

1. Build the Docker image:

```bash
docker build -t model-backend .
```

2. Run the container:

```bash
docker run -p 8000:8000 model-backend
```

> The service will be accessible at [http://localhost:8000](http://localhost:8000)

## 🧪 Testing

To run tests (if implemented):

```bash
pytest
```
