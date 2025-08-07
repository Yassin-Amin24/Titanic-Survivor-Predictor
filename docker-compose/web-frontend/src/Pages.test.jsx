global.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AdminPanel from './components/pages/AdminModelList';
import SurvivalCalculator from './components/pages/Calculator';
import CoursesPage from "./components/pages/Courses";
import HomePage from "./components/pages/LandingPage";
import LoginPage from './components/pages/LoginForm';
import RegisterPage from './components/pages/Register';
import Navigation from './components/Navigation';
import axios from 'axios';
import { MemoryRouter, BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';

// --- MOCKS FOR MOST TESTS ---

const mockLogin = vi.fn();
const mockRegister = vi.fn(() => Promise.resolve({ success: true }));
const mockLogout = vi.fn();

let mockUser = { id: 1, email: 'admin@test.com', is_admin: true };
let mockIsAuthenticated = true;
let mockIsAdmin = true;
let mockPathname = '/';

// Mock react-router-dom navigation/location for all tests
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useLocation: () => ({ pathname: mockPathname }),
  };
});

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}));

// Mock useAuth
vi.mock('./contexts/AuthContext', async () => {
  const original = await vi.importActual('./contexts/AuthContext');
  return {
    ...original,
    useAuth: () => ({
      login: mockLogin,
      register: mockRegister,
      logout: mockLogout,
      user: mockUser,
      isAuthenticated: mockIsAuthenticated,
      isAdmin: mockIsAdmin,
    }),
  };
});

// --- Test Data ---

const mockModels = [
  { id: 1, name: 'Random Forest', algorithm: 'random_forest', accuracy: 0.85, features: ['age'], created_at: new Date().toISOString(), is_default: false },
  { id: 2, name: 'SVM', algorithm: 'svm', accuracy: 0.75, features: ['age', 'fare'], created_at: new Date().toISOString(), is_default: true }
];
const mockUsers = [
  { id: 1, email: 'admin@test.com', created_at: new Date().toISOString(), is_admin: true },
  { id: 2, email: 'user@test.com', created_at: new Date().toISOString(), is_admin: false }
];
const mockFeatures = {
  features: [
    { name: 'age', description: 'Age of the passenger' },
    { name: 'fare', description: 'Fare paid' }
  ]
};

// --- COMPONENT TESTS ---


// Tests for AdminModelList.jsx
describe('AdminPanel Component', () => {
  beforeEach(() => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/models')) return Promise.resolve({ data: mockModels });
      if (url.includes('/users')) return Promise.resolve({ data: mockUsers });
      if (url.includes('/features')) return Promise.resolve({ data: mockFeatures });
    });
  });

  it('renders the AdminPanel page with models and users', async () => {
    render(
      <AuthProvider>
        <AdminPanel />
      </AuthProvider>
    );
    expect(await screen.findByText('Admin Panel')).toBeInTheDocument();
    expect(await screen.findByText('Trained Models')).toBeInTheDocument();
    expect(await screen.findByText('User Management')).toBeInTheDocument();
  });
});


// Tests for Calculator.jsx
describe('SurvivalCalculator Component', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({ data: mockModels });
    axios.post.mockResolvedValue({
      data: {
        predictions: {
          'Random Forest': {
            prediction: 'Survived',
            prediction_value: 1,
            probability: { survived: 0.9, died: 0.1 }
          }
        }
      }
    });
  });

  it('renders SurvivalCalculator and changes age input', async () => {
    render(
      <AuthProvider>
        <SurvivalCalculator />
      </AuthProvider>
    );
    expect(await screen.findByText('Titanic Survival Calculator')).toBeInTheDocument();
    const ageInput = await screen.findByLabelText(/age/i);
    fireEvent.change(ageInput, { target: { value: 42 } });
    expect(ageInput.value).toBe("42");
  });
});


// Tests for Courses.jsx
describe("CoursesPage Component", () => {
  it("renders the CoursesPage and displays course titles", () => {
    render(
      <MemoryRouter>
        <CoursesPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/AI-Powered Web Applications Masterclass/i)).toBeInTheDocument();
    expect(screen.getByText(/Machine Learning Fundamentals/i)).toBeInTheDocument();
    expect(screen.getByText(/Advanced Deep Learning/i)).toBeInTheDocument();
  });

  it("renders testimonials", () => {
    render(
      <BrowserRouter>
        <CoursesPage />
      </BrowserRouter>
    );
    expect(screen.getByText(/Emily Johnson/i)).toBeInTheDocument();
    expect(screen.getByText(/David Kim/i)).toBeInTheDocument();
    expect(screen.getByText(/Maria Garcia/i)).toBeInTheDocument();
  });
});


// Tests for LandingPage.jsx
describe("LandingPage Component", () => {
  it("renders the LandingPage and displays hero title", () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    expect(screen.getByText(/Titanic Survivor Predictor/i)).toBeInTheDocument();
  });

  it("has working call-to-action buttons", () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    expect(screen.getByRole("button", { name: /Try the Predictor/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Explore AI Courses/i })).toBeInTheDocument();
  });
});


// Tests for LoginForm.jsx
describe('LoginPage Component', () => {
  beforeEach(() => {
    mockLogin.mockReset();
    mockNavigate.mockReset();
    mockUser = { id: 1, email: 'admin@test.com', is_admin: true };
    mockIsAuthenticated = true;
    mockIsAdmin = true;
  });

  it('renders the LoginPage form with email and password fields', () => {
    render(
      <AuthProvider>
        <MemoryRouter>
          <LoginPage />
        </MemoryRouter>
      </AuthProvider>
    );
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('handles successful form submission and navigates', async () => {
    mockLogin.mockResolvedValue({ success: true });

    render(
      <AuthProvider>
        <MemoryRouter>
          <LoginPage />
        </MemoryRouter>
      </AuthProvider>
    );

    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'admin@titanic.com' } });
    fireEvent.change(screen.getByLabelText(/^password$/i), { target: { value: 'admin123' } });

    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('admin@titanic.com', 'admin123');
      expect(mockNavigate).toHaveBeenCalledWith('/calculator');
    });
  });

  it('shows error on failed login', async () => {
    mockLogin.mockResolvedValue({ success: false, error: 'Invalid credentials' });

    render(
      <AuthProvider>
        <MemoryRouter>
          <LoginPage />
        </MemoryRouter>
      </AuthProvider>
    );

    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'wrong@user.com' } });
    fireEvent.change(screen.getByLabelText(/^password$/i), { target: { value: 'wrongpass' } });

    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/invalid credentials/i)).toBeInTheDocument();
    expect(mockNavigate).not.toHaveBeenCalled();
  });
});


// Tests for Register.jsx
describe('RegisterPage Component', () => {
  beforeEach(() => {
    mockRegister.mockReset();
    mockUser = { id: 1, email: 'admin@test.com', is_admin: true };
    mockIsAuthenticated = true;
    mockIsAdmin = true;
  });

  it('renders the RegisterPage form with required fields', () => {
    render(
      <AuthProvider>
        <MemoryRouter>
          <RegisterPage />
        </MemoryRouter>
      </AuthProvider>
    );
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
  });

  it('handles registration form input and submission', () => {
    render(
      <AuthProvider>
        <MemoryRouter>
          <RegisterPage />
        </MemoryRouter>
      </AuthProvider>
    );
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmPasswordInput = screen.getByLabelText(/confirm password/i);
    const registerButton = screen.getByRole('button', { name: /create account/i });

    fireEvent.change(emailInput, { target: { value: 'newuser@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'securepass' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'securepass' } });
    fireEvent.click(registerButton);

    expect(emailInput.value).toBe('newuser@example.com');
    expect(passwordInput.value).toBe('securepass');
    expect(confirmPasswordInput.value).toBe('securepass');
  });
});


// Tests for Navigation.jsx
describe('Navigation component', () => {
  beforeEach(() => {
    mockLogout.mockReset();
    mockUser = null;
    mockIsAuthenticated = false;
    mockIsAdmin = false;
    mockPathname = '/';
  });

  test('renders main navigation links', () => {
    render(
      <AuthProvider>
        <MemoryRouter>
          <Navigation />
        </MemoryRouter>
      </AuthProvider>
    );

    expect(screen.getByRole('link', { name: /Home/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Survival Calculator/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /AI Courses/i })).toBeInTheDocument();
  });

  test('highlights the active link based on current pathname', () => {
    mockPathname = '/calculator';

    render(
      <AuthProvider>
        <MemoryRouter>
          <Navigation />
        </MemoryRouter>
      </AuthProvider>
    );

    const activeLink = screen.getByRole('link', { name: /Survival Calculator/i });
    expect(activeLink).toHaveClass('bg-blue-100');
    expect(activeLink).toHaveClass('text-blue-700');
  });

  test('shows login and register buttons when not authenticated', () => {
    mockIsAuthenticated = false;

    render(
      <AuthProvider>
        <MemoryRouter>
          <Navigation />
        </MemoryRouter>
      </AuthProvider>
    );

    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Register/i })).toBeInTheDocument();
    expect(screen.queryByText(/Logout/i)).not.toBeInTheDocument();
  });

  test('shows user email, logout button and admin link if authenticated and admin', () => {
    mockIsAuthenticated = true;
    mockIsAdmin = true;
    mockUser = { email: 'admin@titanic.com' };

    render(
      <AuthProvider>
        <MemoryRouter>
          <Navigation />
        </MemoryRouter>
      </AuthProvider>
    );

    expect(screen.getByText(content => content.includes('admin@titanic.com'))).toBeInTheDocument();
    const logoutButton = screen.queryByRole('button', { name: /logout/i }) || screen.queryByText(/logout/i);
    expect(logoutButton).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Admin/i })).toBeInTheDocument();
  });

  test('shows user email and logout button but no admin link if authenticated and not admin', () => {
    mockIsAuthenticated = true;
    mockIsAdmin = false;
    mockUser = { email: 'user@titanic.com' };

    render(
      <AuthProvider>
        <MemoryRouter>
          <Navigation />
        </MemoryRouter>
      </AuthProvider>
    );

    expect(screen.getByText(content => content.includes('user@titanic.com'))).toBeInTheDocument();
    const logoutButton = screen.queryByRole('button', { name: /logout/i }) || screen.queryByText(/logout/i);
    expect(logoutButton).toBeInTheDocument();
    expect(screen.queryByRole('link', { name: /Admin/i })).not.toBeInTheDocument();
  });

  test('calls logout function when logout button is clicked', () => {
    mockIsAuthenticated = true;
    mockUser = { email: 'user@titanic.com' };

    render(
      <AuthProvider>
        <MemoryRouter>
          <Navigation />
        </MemoryRouter>
      </AuthProvider>
    );

    const logoutButton = screen.queryByRole('button', { name: /logout/i }) || screen.queryByText(/logout/i);
    expect(logoutButton).toBeInTheDocument();

    fireEvent.click(logoutButton);

    expect(mockLogout).toHaveBeenCalledTimes(1);
  });
});
