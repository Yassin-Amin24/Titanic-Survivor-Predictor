import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import App from './App';

// ✅ Correct mock format with `default` key for all components
vi.mock('./components/Navigation', () => ({
  default: () => <div>Mock Navigation</div>,
}));
vi.mock('./components/pages/LandingPage', () => ({
  default: () => <div>Landing Page</div>,
}));
vi.mock('./components/pages/LoginForm', () => ({
  default: () => <div>Login Page</div>,
}));
vi.mock('./components/pages/Register', () => ({
  default: () => <div>Register Page</div>,
}));
vi.mock('./components/pages/Calculator', () => ({
  default: () => <div>Calculator Page</div>,
}));
vi.mock('./components/pages/Courses', () => ({
  default: () => <div>Courses Page</div>,
}));
vi.mock('./components/pages/AdminModelList', () => ({
  default: () => <div>Admin Panel</div>,
}));
vi.mock('./contexts/AuthContext', () => ({
  AuthProvider: ({ children }) => <>{children}</>,
}));

describe('App', () => {
  beforeEach(() => {
    // Reset to root path before each test
    window.history.pushState({}, '', '/');
  });

  it('renders the navigation and landing page by default', () => {
    render(<App />);
    expect(screen.getByText('Mock Navigation')).toBeInTheDocument();
    expect(screen.getByText('Landing Page')).toBeInTheDocument();
  });

  it('renders login page on /login route', () => {
    window.history.pushState({}, '', '/login');
    render(<App />);
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('renders register page on /register route', () => {
    window.history.pushState({}, '', '/register');
    render(<App />);
    expect(screen.getByText('Register Page')).toBeInTheDocument();
  });

  it('renders calculator page on /calculator route', () => {
    window.history.pushState({}, '', '/calculator');
    render(<App />);
    expect(screen.getByText('Calculator Page')).toBeInTheDocument();
  });

  it('renders courses page on /courses route', () => {
    window.history.pushState({}, '', '/courses');
    render(<App />);
    expect(screen.getByText('Courses Page')).toBeInTheDocument();
  });

  it('renders admin panel on /admin route', () => {
    window.history.pushState({}, '', '/admin');
    render(<App />);
    expect(screen.getByText('Admin Panel')).toBeInTheDocument();
  });

  it('redirects unknown route to home page', () => {
    window.history.pushState({}, '', '/unknown');
    render(<App />);
    expect(screen.getByText('Landing Page')).toBeInTheDocument();
  });
});
