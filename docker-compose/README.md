# Docker Compose – Titanic Survival Prediction Application

This repository orchestrates the full AI-powered Titanic Survival Prediction web application using Docker Compose. It integrates the web-frontend, web-backend, model-backend, and database services.

## 📦 Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Running the Application

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd docker-compose
```

### 2. Initialize Git submodules (if used)

```bash
git submodule update --init --recursive
```

### 3. Start all services

```bash
docker-compose up --build
```

> This will build and start all containers (frontend, backend, model-backend, and database).

### 4. Access the application

Once running, the application is accessible at:

- 🌐 [http://localhost:8080](http://localhost:8080)

## 🧼 Stopping the Application

To stop all services:

```bash
docker-compose down
```

## 🧪 Testing Pipelines

- Unit, integration, and end-to-end tests should be triggered via GitLab CI as defined in the respective repositories.
- End-to-end tests may be triggered in a nightly pipeline.

---

Ensure your local setup matches the requirements defined in the course documentation (e.g., Ubuntu 24.04 LTS compatibility).
