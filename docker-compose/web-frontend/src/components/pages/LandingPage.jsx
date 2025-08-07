import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Ship, Brain, Users, TrendingUp, ArrowRight, Star } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <Ship className="h-20 w-20 text-blue-600" />
            </div>
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Titanic Survivor Predictor
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Get ready to embark on an exciting journey with our cutting-edge web application, 
              driven by the power of artificial intelligence! Discover if you would have 
              survived the legendary Titanic disaster.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/calculator">
                <Button size="lg" className="text-lg px-8 py-3">
                  Try the Predictor
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link to="/courses">
                <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                  Explore AI Courses
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our AI-powered system analyzes passenger data using advanced machine learning 
              algorithms to predict survival outcomes.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <Users className="h-12 w-12 text-blue-600" />
                </div>
                <CardTitle>Input Passenger Data</CardTitle>
                <CardDescription>
                  Enter details like class, age, gender, and other passenger characteristics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Our intuitive interface allows you to easily input various passenger 
                  parameters that influenced survival rates on the Titanic.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <Brain className="h-12 w-12 text-blue-600" />
                </div>
                <CardTitle>AI Analysis</CardTitle>
                <CardDescription>
                  Multiple machine learning models analyze the data simultaneously
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Choose from Random Forest, SVM, Decision Trees, and other advanced 
                  algorithms to get comprehensive predictions.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <TrendingUp className="h-12 w-12 text-blue-600" />
                </div>
                <CardTitle>Get Results</CardTitle>
                <CardDescription>
                  Receive detailed survival predictions with probability scores
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  View predictions from multiple models and track your prediction 
                  history to explore different scenarios.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* About Section */}
      <div className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                About the Titanic Disaster
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                On April 15, 1912, during her maiden voyage, the widely considered "unsinkable" 
                RMS Titanic sank after colliding with an iceberg. Unfortunately, there weren't 
                enough lifeboats for everyone onboard, resulting in the death of 1502 out of 
                2224 passengers and crew.
              </p>
              <p className="text-lg text-gray-600 mb-8">
                While there was some element of luck involved in surviving, it seems some groups 
                of people were more likely to survive than others. Our AI system helps you 
                understand these patterns and predict survival outcomes.
              </p>
              <Link to="/calculator">
                <Button size="lg">
                  Start Predicting
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
            <div className="bg-white p-8 rounded-lg shadow-lg">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Key Statistics</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Total Passengers & Crew</span>
                  <span className="text-2xl font-bold text-blue-600">2,224</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Survivors</span>
                  <span className="text-2xl font-bold text-green-600">722</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Casualties</span>
                  <span className="text-2xl font-bold text-red-600">1,502</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Survival Rate</span>
                  <span className="text-2xl font-bold text-blue-600">32.5%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-24 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Test Your Survival Chances?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of users who have already discovered their Titanic survival 
            predictions using our advanced AI technology.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/calculator">
              <Button size="lg" variant="secondary" className="text-lg px-8 py-3">
                Start Prediction
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link to="/register">
              <Button size="lg" variant="outline" className="text-lg px-8 py-3 text-white border-white hover:bg-white hover:text-blue-600">
                Create Account
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

