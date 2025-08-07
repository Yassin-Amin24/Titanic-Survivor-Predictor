# Web Frontend – Titanic Survival Prediction

This is the frontend interface for the Titanic Survival Prediction web application, built with React and Vite. It allows users to interact with the survival prediction system, view results, register/login, and manage predictions.

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd web-frontend
```

### 2. Install dependencies

> Ensure [pnpm](https://pnpm.io/) is installed:
```bash
npm install -g pnpm
```

Then install project dependencies:

```bash
pnpm install
```

## 🚀 Run the Application

### Option 1: Run with pnpm (Vite Dev Server)

```bash
pnpm run dev
```

- The app will be available at the URL printed in your terminal, typically [http://localhost:5173](http://localhost:5173)

### Option 2: Run with Docker

1. Build the Docker image:

```bash
docker build -t web-frontend .
```

2. Run the container:

```bash
docker run -p 8080:80 web-frontend
```

> The service will be available at [http://localhost:8080](http://localhost:8080)

## 🧪 Testing

To run tests (if configured):

```bash
pnpm test
```
