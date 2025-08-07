
# Web Backend – Titanic Survival Prediction API

This is the backend service for the Titanic Survival Prediction application. It is built using **FastAPI** and provides API endpoints for user authentication, model management, and survival prediction.

You can run the app either using **Docker** or locally with **Uvicorn**.

---

## 📁 Project Structure

```
web-backend/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── models/           # Pydantic and DB models
│   ├── routes/           # API route definitions
│   ├── services/         # Core business logic
│   └── database/         # SQLAlchemy setup
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image setup
├── docker-compose.yml    # Docker service configuration (if used)
└── README.md             # You're here
```

---

## 🚀 Running the App

### Option 1: Using Docker

> Requires: [Docker](https://docs.docker.com/get-docker/) installed

1. **Build and run the container:**

```bash
docker build -t titanic-backend .
docker run -d -p 8000:8000 titanic-backend
```

2. **Access the API docs**:  
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Using Uvicorn (Local Python Environment)

> Requires: Python 3.8+ and pip

1. **Create a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the server with Uvicorn:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. **Access the API docs**:  
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Environment Variables

Make sure to configure the necessary environment variables (if any) for DB access, JWT keys, or other secrets, either using a `.env` file or directly in your environment.

---

## 📬 Contact

For issues or contributions, feel free to reach out to the development team or open a pull request.
