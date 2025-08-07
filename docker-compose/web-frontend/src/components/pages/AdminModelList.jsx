import React, { useState, useEffect } from 'react';
import { useAuth } from "../../contexts/AuthContext";
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Settings, Trash2, Plus, Brain, Users, Database } from 'lucide-react';
import axios from 'axios';

const AdminPanel = () => {
  const { user, isAdmin } = useAuth();
  const [models, setModels] = useState([]);
  const [users, setUsers] = useState([]);
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // New model training form
  const [newModel, setNewModel] = useState({
    model_name: '',
    algorithm: 'random_forest',
    features: []
  });

  const API_BASE_URL = 'http://localhost:8000';

  const algorithms = [
    { value: 'random_forest', label: 'Random Forest' },
    { value: 'decision_tree', label: 'Decision Tree' },
    { value: 'knn', label: 'K-Nearest Neighbors' },
    { value: 'svm', label: 'Support Vector Machine' },
    { value: 'logistic_regression', label: 'Logistic Regression' },
    { value: 'perceptron', label: 'Perceptron' },
    { value: 'sgd', label: 'Stochastic Gradient Descent' },
    { value: 'gaussian_nb', label: 'Gaussian Naive Bayes' }
  ];

  useEffect(() => {
    if (isAdmin) {
      fetchModels();
      fetchUsers();
      fetchFeatures();
    }
  }, [isAdmin]);

  const fetchModels = async () => {
    try {
      // For admin, get all models
      const defaultModelsResponse = await axios.get(`${API_BASE_URL}/api/models?default_only=true`);
      const customModelsResponse = await axios.get(`${API_BASE_URL}/api/models?custom_only=true`);

      // Combine both types but mark them clearly
      const allModels = [
        ...defaultModelsResponse.data,
        ...customModelsResponse.data
      ];

      setModels(allModels);
    } catch (error) {
      console.error('Error fetching models:', error);
      setError('Failed to fetch models');
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/users`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
      setError('Failed to fetch users');
    }
  };

  const fetchFeatures = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/features`);
      setFeatures(response.data.features || []);
    } catch (error) {
      console.error('Error fetching features:', error);
      setError('Failed to fetch features');
    }
  };

  const deleteModel = async (modelId) => {
    if (!confirm('Are you sure you want to delete this model?')) return;

    try {
      await axios.delete(`${API_BASE_URL}/api/models/${modelId}`);
      setSuccess('Model deleted successfully');
      fetchModels();
    } catch (error) {
      console.error('Error deleting model:', error);
      setError('Failed to delete model');
    }
  };

  const deleteUser = async (userId) => {
    if (!confirm('Are you sure you want to delete this user?')) return;

    try {
      await axios.delete(`${API_BASE_URL}/api/users/${userId}`);
      setSuccess('User deleted successfully');
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
      setError('Failed to delete user');
    }
  };

  const handleFeatureToggle = (featureName, checked) => {
    setNewModel(prev => ({
      ...prev,
      features: checked
        ? [...prev.features, featureName]
        : prev.features.filter(f => f !== featureName)
    }));
  };

  const trainNewModel = async (e) => {
    e.preventDefault();

    if (!newModel.model_name.trim()) {
      setError('Model name is required');
      return;
    }

    if (newModel.features.length === 0) {
      setError('At least one feature must be selected');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_BASE_URL}/api/models/train`, newModel);
      setSuccess('Model trained successfully');
      setNewModel({
        model_name: '',
        algorithm: 'random_forest',
        features: []
      });
      fetchModels();
    } catch (error) {
      console.error('Error training model:', error);
      setError('Failed to train model');
    }

    setLoading(false);
  };

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>
              You need admin privileges to access this page.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Panel</h1>
          <p className="text-gray-600">Manage models, users, and system settings</p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="mb-6">
            <AlertDescription>{success}</AlertDescription>
          </Alert>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Models Management */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="mr-2 h-5 w-5" />
                  Trained Models
                </CardTitle>
                <CardDescription>
                  View and manage all trained machine learning models
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {models.map((model) => (
                    <div key={model.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-medium">{model.name}</h4>
                          {model.is_default && (
                            <Badge variant="secondary">Default</Badge>
                          )}
                        </div>
                        <div className="text-sm text-gray-600">
                          <div>Algorithm: {model.algorithm}</div>
                          <div>Accuracy: {(model.accuracy * 100).toFixed(1)}%</div>
                          <div>Features: {model.features.length}</div>
                          <div>Created: {new Date(model.created_at).toLocaleDateString()}</div>
                        </div>
                      </div>
                      {!model.is_default && (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => deleteModel(model.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Train New Model */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plus className="mr-2 h-5 w-5" />
                  Train New Model
                </CardTitle>
                <CardDescription>
                  Create a new machine learning model with custom features
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={trainNewModel} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="model_name">Model Name</Label>
                    <Input
                      id="model_name"
                      value={newModel.model_name}
                      onChange={(e) => setNewModel(prev => ({ ...prev, model_name: e.target.value }))}
                      placeholder="Enter model name"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="algorithm">Algorithm</Label>
                    <Select
                      value={newModel.algorithm}
                      onValueChange={(value) => setNewModel(prev => ({ ...prev, algorithm: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-white border border-gray-200 shadow-lg">
                        {algorithms.map((algo) => (
                          <SelectItem key={algo.value} value={algo.value} className="py-2 hover:bg-gray-100">
                            {algo.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Features</Label>
                    <div className="space-y-2 max-h-48 overflow-y-auto border rounded p-3">
                      {features.map((feature) => (
                        <div key={feature.name} className="flex items-center space-x-2">
                          <Checkbox
                            checked={newModel.features.includes(feature.name)}
                            onCheckedChange={(checked) => handleFeatureToggle(feature.name, checked)}
                          />
                          <div className="flex-1">
                            <Label className="text-sm font-medium">{feature.name}</Label>
                            <div className="text-xs text-gray-500">{feature.description}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <Button type="submit" disabled={loading} className="w-full">
                    {loading ? 'Training Model...' : 'Train Model'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Users Management */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="mr-2 h-5 w-5" />
                  User Management
                </CardTitle>
                <CardDescription>
                  View and manage all registered users
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {users.map((userItem) => (
                    <div key={userItem.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-medium">{userItem.email}</h4>
                          {userItem.is_admin && (
                            <Badge variant="destructive">Admin</Badge>
                          )}
                        </div>
                        <div className="text-sm text-gray-600">
                          <div>ID: {userItem.id}</div>
                          <div>Created: {new Date(userItem.created_at).toLocaleDateString()}</div>
                        </div>
                      </div>
                      {userItem.id !== user.id && (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => deleteUser(userItem.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* System Stats */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Database className="mr-2 h-5 w-5" />
                  System Statistics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{models.length}</div>
                    <div className="text-sm text-gray-600">Total Models</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{users.length}</div>
                    <div className="text-sm text-gray-600">Total Users</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                      {models.filter(m => m.is_default).length}
                    </div>
                    <div className="text-sm text-gray-600">Default Models</div>
                  </div>
                  <div className="text-center p-4 bg-orange-50 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">
                      {users.filter(u => u.is_admin).length}
                    </div>
                    <div className="text-sm text-gray-600">Admin Users</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;