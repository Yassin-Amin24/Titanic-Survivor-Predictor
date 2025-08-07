import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navigation from './components/Navigation';
import HomePage from './components/pages/LandingPage';
import LoginPage from './components/pages/LoginForm';
import RegisterPage from './components/pages/Register';
import SurvivalCalculator from './components/pages/Calculator';
import CoursesPage from './components/pages/Courses';
import AdminPanel from './components/pages/AdminModelList';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navigation />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/calculator" element={<SurvivalCalculator />} />
            <Route path="/courses" element={<CoursesPage />} />
            <Route path="/admin" element={<AdminPanel />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

