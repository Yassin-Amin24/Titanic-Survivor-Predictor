import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Ship, User, LogOut, Settings } from 'lucide-react';

const Navigation = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Ship className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">Titanic Predictor</span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
              }`}
            >
              Home
            </Link>

            <Link
              to="/calculator"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/calculator') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
              }`}
            >
              Survival Calculator
            </Link>

            <Link
              to="/courses"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/courses') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
              }`}
            >
              AI Courses
            </Link>

            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                {isAdmin && (
                  <Link
                    to="/admin"
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive('/admin') 
                        ? 'bg-blue-100 text-blue-700' 
                        : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
                    }`}
                  >
                    <Settings className="h-4 w-4 inline mr-1" />
                    Admin
                  </Link>
                )}
                
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <User className="h-4 w-4" />
                  <span>{user?.email}</span>
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center space-x-1"
                >
                  <LogOut className="h-4 w-4" />
                  <span>Logout</span>
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login">
                  <Button variant="outline" size="sm">
                    Login
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">
                    Register
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

