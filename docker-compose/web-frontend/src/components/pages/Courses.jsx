import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Brain, 
  Users, 
  TrendingUp, 
  Award, 
  BookOpen, 
  Video, 
  FileText, 
  Star,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const CoursesPage = () => {
  const courses = [
    {
      id: 1,
      title: "AI-Powered Web Applications Masterclass",
      description: "Learn to build cutting-edge web applications powered by artificial intelligence, just like our Titanic Predictor!",
      level: "Intermediate",
      duration: "12 weeks",
      price: "$299",
      rating: 4.9,
      students: 2847,
      features: [
        "Build 5 real-world AI web applications",
        "Master FastAPI and React integration",
        "Deploy ML models in production",
        "Advanced data visualization techniques",
        "User authentication and security",
        "Docker containerization"
      ],
      instructor: "Dr. Sarah Chen",
      badge: "Most Popular"
    },
    {
      id: 2,
      title: "Machine Learning Fundamentals",
      description: "Start your AI journey with comprehensive machine learning foundations using real datasets like Titanic.",
      level: "Beginner",
      duration: "8 weeks",
      price: "$199",
      rating: 4.8,
      students: 5234,
      features: [
        "Supervised and unsupervised learning",
        "Data preprocessing and feature engineering",
        "Model evaluation and selection",
        "Hands-on projects with real datasets",
        "Python and scikit-learn mastery",
        "Statistical analysis fundamentals"
      ],
      instructor: "Prof. Michael Rodriguez",
      badge: "Beginner Friendly"
    },
    {
      id: 3,
      title: "Advanced Deep Learning",
      description: "Dive deep into neural networks, computer vision, and natural language processing with practical applications.",
      level: "Advanced",
      duration: "16 weeks",
      price: "$499",
      rating: 4.9,
      students: 1456,
      features: [
        "Neural networks from scratch",
        "Convolutional Neural Networks (CNNs)",
        "Recurrent Neural Networks (RNNs)",
        "Transformer architectures",
        "Computer vision projects",
        "NLP applications"
      ],
      instructor: "Dr. Alex Thompson",
      badge: "Expert Level"
    }
  ];

  const testimonials = [
    {
      name: "Emily Johnson",
      role: "Software Engineer at TechCorp",
      content: "This course transformed my career! I went from knowing nothing about AI to building production-ready applications.",
      rating: 5
    },
    {
      name: "David Kim",
      role: "Data Scientist at StartupXYZ",
      content: "The hands-on approach and real-world projects made all the difference. Highly recommended!",
      rating: 5
    },
    {
      name: "Maria Garcia",
      role: "Product Manager at InnovateCo",
      content: "Even as a non-technical person, I was able to understand and apply AI concepts to my work.",
      rating: 5
    }
  ];

  const getBadgeVariant = (badge) => {
    switch (badge) {
      case "Most Popular": return "default";
      case "Beginner Friendly": return "secondary";
      case "Expert Level": return "destructive";
      default: return "outline";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Master AI-Powered Web Development
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto opacity-90">
            Join thousands of students learning to build intelligent web applications. 
            From machine learning basics to production deployment - we've got you covered!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" className="text-lg px-8 py-3">
              Browse Courses
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8 py-3 text-white border-white hover:bg-white hover:text-blue-600">
              Free Preview
            </Button>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">10,000+</div>
              <div className="text-gray-600">Students Enrolled</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">95%</div>
              <div className="text-gray-600">Completion Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">4.9/5</div>
              <div className="text-gray-600">Average Rating</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">500+</div>
              <div className="text-gray-600">Career Changes</div>
            </div>
          </div>
        </div>
      </div>

      {/* Courses Section */}
      <div className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Our Featured Courses
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Comprehensive courses designed to take you from beginner to expert in AI web development
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {courses.map((course) => (
              <Card key={course.id} className="relative overflow-hidden">
                {course.badge && (
                  <div className="absolute top-4 right-4 z-10">
                    <Badge variant={getBadgeVariant(course.badge)}>
                      {course.badge}
                    </Badge>
                  </div>
                )}
                
                <CardHeader>
                  <CardTitle className="text-xl mb-2">{course.title}</CardTitle>
                  <CardDescription className="text-base">
                    {course.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-4">
                      <Badge variant="outline">{course.level}</Badge>
                      <span className="text-gray-600">{course.duration}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="font-medium">{course.rating}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center">
                      <Users className="h-4 w-4 mr-1" />
                      {course.students.toLocaleString()} students
                    </div>
                    <div className="text-2xl font-bold text-blue-600">
                      {course.price}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <h4 className="font-medium text-sm">What you'll learn:</h4>
                    <ul className="space-y-1">
                      {course.features.slice(0, 3).map((feature, index) => (
                        <li key={index} className="flex items-center text-sm text-gray-600">
                          <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                          {feature}
                        </li>
                      ))}
                      {course.features.length > 3 && (
                        <li className="text-sm text-gray-500">
                          +{course.features.length - 3} more topics
                        </li>
                      )}
                    </ul>
                  </div>

                  <div className="pt-4 border-t">
                    <div className="flex items-center justify-between mb-4">
                      <div className="text-sm text-gray-600">
                        Instructor: <span className="font-medium">{course.instructor}</span>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button className="flex-1">
                        Enroll Now
                      </Button>
                      <Button variant="outline" size="sm">
                        Preview
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Our Courses?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We provide comprehensive, hands-on learning experiences that prepare you for real-world challenges
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Hands-on Projects</h3>
              <p className="text-gray-600">Build real applications like our Titanic Predictor</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Video className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Video Lessons</h3>
              <p className="text-gray-600">High-quality video content with expert instructors</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Community Support</h3>
              <p className="text-gray-600">Join a community of learners and experts</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Certificates</h3>
              <p className="text-gray-600">Earn industry-recognized certificates</p>
            </div>
          </div>
        </div>
      </div>

      {/* Testimonials */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              What Our Students Say
            </h2>
            <p className="text-xl text-gray-600">
              Join thousands of successful graduates who transformed their careers
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index}>
                <CardContent className="pt-6">
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                  <div>
                    <div className="font-semibold">{testimonial.name}</div>
                    <div className="text-sm text-gray-500">{testimonial.role}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Start Your AI Journey?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join our community of learners and start building intelligent web applications today. 
            Your future in AI starts here!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" variant="secondary" className="text-lg px-8 py-3">
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="text-lg px-8 py-3 text-white border-white hover:bg-white hover:text-blue-600">
              View All Courses
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoursesPage;

