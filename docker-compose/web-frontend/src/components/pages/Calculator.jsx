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
import { Calculator, RotateCcw, Info, History, Brain } from 'lucide-react';
import axios from 'axios';

const SurvivalCalculator = () => {
  const { user, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState([]);
  const [predictions, setPredictions] = useState({});
  const [history, setHistory] = useState([]);
  const [showExplanations, setShowExplanations] = useState({});

  // Form state
const [formData, setFormData] = useState({
  pclass: 3,
  sex: "male",
  age: 25,
  sibsp: 0,
  parch: 0,
  fare: 50,
  embarked: "S",
  title: "Mr",
});

  // Selected models
  const [selectedModels, setSelectedModels] = useState([]);

  const API_BASE_URL = 'http://localhost:8000';

  // Feature explanations
  const explanations = {
    pclass: "Passenger class was a proxy for socio-economic status. First class passengers had better access to lifeboats.",
    sex: "Women and children were given priority during the evacuation ('women and children first' policy).",
    age: "Children were prioritized for lifeboats. Age also affected physical ability to survive in cold water.",
    fare: "Higher fares often correlated with better cabin locations and easier access to lifeboats.",
    traveled_alone: "Passengers traveling with family members might have delayed evacuation to stay together.",
    embarked: "Port of embarkation could indicate passenger's origin and potentially their cabin location.",
    title: "Titles extracted from names indicate social status and age group, affecting survival chances."
  };

  useEffect(() => {
    fetchModels();
    if (isAuthenticated) {
      fetchHistory();
    }
  }, [isAuthenticated]);

  // Update the fetchModels function to initially load only default models
  const fetchModels = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/models`);

      // Ensure we have data and it's an array
      const modelData = Array.isArray(response.data) ? response.data : [];

      // For anonymous users, filter to only show Random Forest and SVM models
      if (!isAuthenticated) {
        const filteredModels = modelData.filter(
          model => model.algorithm === 'random_forest' || model.algorithm === 'svm'
        );
        setModels(filteredModels);

        // Select first model by default if available
        if (filteredModels.length > 0) {
          setSelectedModels([filteredModels[0].name]);
        }
      } else {
        // For authenticated users, show all models
        setModels(modelData);

        // Select first model by default if available
        if (modelData.length > 0) {
          setSelectedModels([modelData[0].name]);
        }
      }
    } catch (error) {
      console.error('Error fetching models:', error);
      setModels([]);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/history`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };


  const handleInputChange = (field, value) => {
    // Special handling for family-related fields
    if (field === 'traveled_alone') {
      // If setting to traveled alone, reset family fields
      if (value === true) {
        setFormData(prev => ({
          ...prev,
          [field]: value,
          sibsp: 0,
          parch: 0
        }));
      } else {
        setFormData(prev => ({
          ...prev,
          [field]: value
        }));
      }
    } else if (field === 'children_traveled_with') {
      // Map children_traveled_with to parch
      setFormData(prev => ({
        ...prev,
        parch: value
      }));
    } else if (field === 'siblings_traveled_with') {
      // Map siblings_traveled_with to sibsp
      setFormData(prev => ({
        ...prev,
        sibsp: value
      }));
    } else {
      // Normal field update
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const handleModelSelection = (modelName, checked) => {
    if (!isAuthenticated) {
      // For anonymous users, limit to 2 models
      if (checked) {
        setSelectedModels(prev => {
          // If already have 2 models, replace the oldest one
          if (prev.length >= 2) {
            return [...prev.slice(1), modelName];
          } else {
            return [...prev, modelName];
          }
        });
      } else {
        // If unchecking, just remove that model
        setSelectedModels(prev => prev.filter(m => m !== modelName));
      }
    } else {
      // For logged in users, no limit
      setSelectedModels(prev => {
        if (checked) {
          return [...prev, modelName];
        } else {
          return prev.filter(m => m !== modelName);
        }
      });
    }
  };

  const makePrediction = async () => {
    if (selectedModels.length === 0) return;

  setLoading(true);
  try {
    const response = await axios.post(`${API_BASE_URL}/api/predict`, {
      passenger: { ...formData, cabin_letter: "U" },
      model_names: selectedModels
    });

    setPredictions(response.data.predictions);

    if (isAuthenticated) {
      fetchHistory();
    }
  } catch (error) {
    console.error("Prediction error:", error);
    if (error.response) {
    console.error("Response status:", error.response.status);
    console.error("Response data:", error.response.data); // ✅ this will show validation error from FastAPI
    }
  }
  setLoading(false);
};

  const resetForm = () => {
    setFormData({
      pclass: 3,
      sex: 'male',
      age: 30,
      fare: 50,
      sibsp: 1,
      parch: 1,
      embarked: 'S',
      title: 'Mr',
      cabin_letter: 'U'
    });
    setPredictions({});
  };

  const toggleExplanation = (field) => {
    setShowExplanations(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Titanic Survival Calculator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Enter passenger details to predict survival chances using advanced machine learning models
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Input Form */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calculator className="mr-2 h-5 w-5" />
                  Passenger Information
                </CardTitle>
                <CardDescription>
                  Enter the passenger details to get survival predictions
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Passenger Class */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="pclass">Passenger Class</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('pclass')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <Select
                    value={formData.pclass.toString()}
                    onValueChange={(value) => handleInputChange('pclass', parseInt(value))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-[#f9fafb] p-0">
                      {[
                        { value: "1", label: "First Class" },
                        { value: "2", label: "Second Class" },
                        { value: "3", label: "Third Class" }
                      ].map((item, index) => (
                        <SelectItem
                          key={item.value}
                          value={item.value}
                          className={`px-3 py-2 hover:bg-gray-100 aria-selected:bg-gray-200 ${
                            index !== 0 ? "border-t border-black" : ""
                          }`}
                        >
                          {item.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {showExplanations.pclass && (
                    <Alert>
                      <AlertDescription>{explanations.pclass}</AlertDescription>
                    </Alert>
                  )}
                </div>

                {/* Sex */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="sex">Gender</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('sex')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <Select
                    value={formData.sex}
                    onValueChange={(value) => handleInputChange('sex', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-[#f9fafb] p-0">
                      {["male", "female"].map((gender, index) => (
                        <SelectItem
                          key={gender}
                          value={gender}
                          className={`px-3 py-2 hover:bg-gray-100 aria-selected:bg-gray-200 ${
                            index !== 0 ? "border-t border-black" : ""
                          }`}
                        >
                          {gender.charAt(0).toUpperCase() + gender.slice(1)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {showExplanations.sex && (
                    <Alert>
                      <AlertDescription>{explanations.sex}</AlertDescription>
                    </Alert>
                  )}
                </div>


                {/* Age */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="age">Age (0-100)</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('age')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <Input
                    id="age"
                    name="age"
                    type="number"
                    min="0"
                    max="100"
                    value={formData.age}
                    onChange={(e) => handleInputChange('age', parseInt(e.target.value) || 0)}
                  />
                  {showExplanations.age && (
                    <Alert>
                      <AlertDescription>{explanations.age}</AlertDescription>
                    </Alert>
                  )}
                </div>

                {/* Fare */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="fare">Ticket Fare ($0-500)</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('fare')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <Input
                    type="number"
                    min="0"
                    max="500"
                    step="0.01"
                    value={formData.fare}
                    onChange={(e) => handleInputChange('fare', parseFloat(e.target.value) || 0)}
                  />
                  {showExplanations.fare && (
                    <Alert>
                      <AlertDescription>{explanations.fare}</AlertDescription>
                    </Alert>
                  )}
                </div>

                {/*/!* Cabin Letter *!/*/}
                {/*<div className="space-y-2">*/}
                {/*  <div className="flex items-center justify-between">*/}
                {/*    <Label htmlFor="cabin">Cabin Letter</Label>*/}
                {/*  </div>*/}
                {/*  <Select*/}
                {/*    value={formData.cabin_letter || ""}*/}
                {/*    onValueChange={(value) => handleInputChange("cabin_letter", value)}*/}
                {/*  >*/}
                {/*    <SelectTrigger>*/}
                {/*      <SelectValue placeholder="Select Cabin Letter" />*/}
                {/*    </SelectTrigger>*/}
                {/*    <SelectContent className="bg-[#f9fafb] p-0">*/}
                {/*      {["A", "B", "C", "D", "E", "F", "G", "U"].map((letter, index) => (*/}
                {/*        <SelectItem*/}
                {/*          key={letter}*/}
                {/*          value={letter}*/}
                {/*          className={`px-3 py-2 ${*/}
                {/*            index !== 0 ? "border-t border-black" : ""*/}
                {/*          }`}*/}
                {/*        >*/}
                {/*          {letter}*/}
                {/*        </SelectItem>*/}
                {/*      ))}*/}
                {/*    </SelectContent>*/}
                {/*  </Select>*/}
                {/*</div>*/}

                {/* Traveled Alone */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>Traveled Alone</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('traveled_alone')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      checked={formData.traveled_alone}
                      onCheckedChange={(checked) => handleInputChange('traveled_alone', checked)}
                    />
                    <Label>Yes, traveled alone</Label>
                  </div>
                  {showExplanations.traveled_alone && (
                    <Alert>
                      <AlertDescription>{explanations.traveled_alone}</AlertDescription>
                    </Alert>
                  )}
                </div>

                {/* Children & Siblings fields appear only if NOT traveled alone */}
                {!formData.traveled_alone && (
                  <>
                    {/* Children Traveled With (parch)*/}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="parch">Parents/Children Traveled With</Label>
                      </div>
                      <Input
                          type="number"
                          id="parch"
                          min="0"
                          max="10"
                          step="1"
                          value={formData.parch || 0}
                          onChange={(e) =>
                              handleInputChange('parch', parseInt(e.target.value) || 0)
                          }
                      />
                      <div className="text-xs text-gray-500">Number of parents or children traveling with this
                        passenger
                      </div>
                    </div>

                    {/* Siblings (sibsp)*/}
                    <div className="space-y-2">
                      <Label htmlFor="sibsp">Siblings Traveled With</Label>
                      <Input
                          id="sibsp"
                          type="number"
                          min="0"
                          value={formData.sibsp || 0}
                          onChange={(e) =>
                              handleInputChange("sibsp", parseInt(e.target.value) || 0)
                          }
                      />
                      <div className="text-xs text-gray-500">Number of siblings or spouse aboard</div>
                    </div>
                  </>
                )}

                {/* Embarked */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="embarked">Port of Embarkation</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('embarked')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <Select
                    value={formData.embarked}
                    onValueChange={(value) => handleInputChange('embarked', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-[#f9fafb] p-0">
                      {["C", "Q", "S"].map((value, index) => (
                        <SelectItem
                          key={value}
                          value={value}
                          className={`px-3 py-2 hover:bg-gray-100 aria-selected:bg-gray-200 ${
                            index !== 0 ? "border-t border-black" : ""
                          }`}
                        >
                          {{
                            C: "Cherbourg",
                            Q: "Queenstown",
                            S: "Southampton"
                          }[value]}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {showExplanations.embarked && (
                    <Alert>
                      <AlertDescription>{explanations.embarked}</AlertDescription>
                    </Alert>
                  )}
                </div>


                {/* Title */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="title">Title</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation('title')}
                    >
                      <Info className="h-4 w-4" />
                    </Button>
                  </div>
                  <Select
                    value={formData.title}
                    onValueChange={(value) => handleInputChange('title', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-[#f9fafb] p-0">
                      {["Master", "Miss", "Mr", "Mrs", "Rare"].map((title, index) => (
                        <SelectItem
                          key={title}
                          value={title}
                          className={`px-3 py-2 hover:bg-gray-100 aria-selected:bg-gray-200 ${
                            index !== 0 ? "border-t border-black" : ""
                          }`}
                        >
                          {title}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {showExplanations.title && (
                    <Alert>
                      <AlertDescription>{explanations.title}</AlertDescription>
                    </Alert>
                  )}
                </div>


                <div className="flex space-x-4">
                  <Button onClick={makePrediction} disabled={loading || selectedModels.length === 0}>
                    {loading ? 'Predicting...' : 'Predict Survival'}
                  </Button>
                  <Button variant="outline" onClick={resetForm}>
                    <RotateCcw className="mr-2 h-4 w-4" />
                    Reset
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Results and Model Selection */}
          <div className="space-y-6">
            {/* Model Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="mr-2 h-5 w-5" />
                  Model Selection
                </CardTitle>
                <CardDescription>
                  {isAuthenticated
                    ? "Select any combination of models"
                    : "Anonymous users can select up to 2 models"
                  }
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {models.map((model) => (
                    <div key={model.id} className="flex items-center space-x-2">
                      <Checkbox
                        checked={selectedModels.includes(model.name)}
                        onCheckedChange={(checked) => handleModelSelection(model.name, checked)}
                        disabled={!isAuthenticated && !selectedModels.includes(model.name) && selectedModels.length >= 2}
                      />
                      <div className="flex-1">
                        <Label className="text-sm font-medium">{model.name}</Label>
                        <div className="text-xs text-gray-500">
                          Accuracy: {(model.accuracy * 100).toFixed(1)}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Predictions */}
            {Object.keys(predictions).length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Predictions</CardTitle>
                  <CardDescription>
                    Survival predictions from selected models
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(predictions).map(([modelName, result]) => (
                      <div key={modelName} className="p-4 border rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium">{modelName}</h4>
                          <Badge variant={result.prediction_value === 1 ? "default" : "destructive"}>
                            {result.prediction}
                          </Badge>
                        </div>
                        {result.probability && (
                          <div className="text-sm text-gray-600">
                            <div>Survival: {(result.probability.survived * 100).toFixed(1)}%</div>
                            <div>Death: {(result.probability.died * 100).toFixed(1)}%</div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* History for logged-in users */}
            {isAuthenticated && history.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <History className="mr-2 h-5 w-5" />
                    Recent Predictions
                  </CardTitle>
                  <CardDescription>
                    Your last 10 predictions
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-64 overflow-y-auto">
                    {history.map((item) => (
                      <div key={item.id} className="p-3 border rounded text-sm">
                        <div className="flex justify-between items-center mb-1">
                          <span className="font-medium">
                            {item.sex}, Age {item.age}, Class {item.pclass}
                          </span>
                          <span className="text-xs text-gray-500">
                            {new Date(item.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="text-xs text-gray-600">
                          Models: {item.model_predictions ? Object.keys(item.model_predictions).length : 0}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SurvivalCalculator;

