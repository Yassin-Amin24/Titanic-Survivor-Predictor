import React from 'react';
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import { AuthProvider, useAuth } from './AuthContext';

vi.mock('axios');

// A test component that consumes AuthContext
const TestComponent = () => {
  const { user, login, register, logout, isAuthenticated, isAdmin, error } = useAuth();

  return (
    <div>
      <p>User: {user ? user.email : 'No user'}</p>
      <p>Authenticated: {isAuthenticated ? 'Yes' : 'No'}</p>
      <p>Admin: {isAdmin ? 'Yes' : 'No'}</p>
      {error && <p data-testid="error">{error}</p>}
      <button onClick={() => login('test@example.com', 'pass')}>Login</button>
      <button onClick={() => register('new@example.com', 'pass')}>Register</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.resetAllMocks();
  });

  it('logs in successfully and updates context', async () => {
    const fakeUser = { email: 'test@example.com', is_admin: false };
    const token = 'fake-token';

    axios.post.mockImplementation((url) => {
      if (url === 'http://localhost:8000/api/auth/login') {
        return Promise.resolve({ data: { user: fakeUser, token } });
      }
      throw new Error('Unexpected URL: ' + url);
    });

    axios.get.mockResolvedValueOnce({ data: { user: fakeUser } });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await act(async () => {
      fireEvent.click(screen.getByText('Login'));
    });

    await waitFor(() => {
      expect(screen.queryByText(`User: ${fakeUser.email}`)).toBeInTheDocument();
    });

    expect(localStorage.getItem('token')).toBe(token);
    expect(screen.getByText('Authenticated: Yes')).toBeInTheDocument();
    expect(screen.getByText('Admin: No')).toBeInTheDocument();
  });

  it('registers successfully and updates context', async () => {
    const fakeUser = { email: 'new@example.com', is_admin: true };
    const token = 'register-token';

    axios.post.mockImplementation((url) => {
      if (url === 'http://localhost:8000/api/auth/register') {
        return Promise.resolve({ data: { user: fakeUser, token } });
      }
      throw new Error('Unexpected URL: ' + url);
    });

    axios.get.mockResolvedValueOnce({ data: { user: fakeUser } });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await act(async () => {
      fireEvent.click(screen.getByText('Register'));
    });

    await waitFor(() => {
      expect(screen.queryByText(`User: ${fakeUser.email}`)).toBeInTheDocument();
    });

    expect(localStorage.getItem('token')).toBe(token);
    expect(screen.getByText('Authenticated: Yes')).toBeInTheDocument();
    expect(screen.getByText('Admin: Yes')).toBeInTheDocument();
  });

  it('logs out and clears context', async () => {
    const fakeUser = { email: 'logout@example.com', is_admin: false };
    const token = 'logout-token';
    localStorage.setItem('token', token);

    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/api/auth/me') {
        return Promise.resolve({ data: { user: fakeUser } });
      }
      throw new Error('Unexpected GET URL: ' + url);
    });

    axios.post.mockImplementation((url) => {
      if (url === 'http://localhost:8000/api/auth/logout') {
        return Promise.resolve({});
      }
      throw new Error('Unexpected POST URL: ' + url);
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() =>
      expect(screen.getByText(`User: ${fakeUser.email}`)).toBeInTheDocument()
    );

    fireEvent.click(screen.getByText('Logout'));

    await waitFor(() => {
      expect(screen.getByText('User: No user')).toBeInTheDocument();
      expect(localStorage.getItem('token')).toBeNull();
    });
  });

  it('shows error on failed login', async () => {
    axios.post.mockRejectedValueOnce({
      response: { data: { detail: 'Invalid credentials' } }
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await act(async () => {
      fireEvent.click(screen.getByText('Login'));
    });

    await waitFor(() => {
      expect(screen.getByTestId('error')).toHaveTextContent(/Invalid credentials/i);
    });
  });

  it('shows error on failed registration', async () => {
    axios.post.mockRejectedValueOnce({
      response: { data: { detail: 'Registration failed' } }
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await act(async () => {
      fireEvent.click(screen.getByText('Register'));
    });

    await waitFor(() => {
      expect(screen.getByTestId('error')).toHaveTextContent(/Registration failed/i);
    });
  });
});
