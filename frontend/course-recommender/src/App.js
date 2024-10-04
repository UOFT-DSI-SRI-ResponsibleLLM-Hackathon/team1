import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import Section from './components/Section';
import './images/banner.png';
import CourseInput from './components/CourseInput';
import RecommendationList from './components/RecommendationList';

// function App() {
//   const [recommendations, setRecommendations] = useState([]);

//   // Mock request to backend (replace this with actual API call later)
//   const getRecommendations = (input) => {
//     // Replace this part with a real API request
//     // fetch('http://your-backend-api.com/api/recommendations', { method: 'POST', body: JSON.stringify({ prompt: input }) })
//     //   .then((response) => response.json())
//     //   .then((data) => setRecommendations(data))
//     //   .catch((error) => console.error('Error fetching recommendations:', error));
    
//     // Temporary mock data for frontend testing
//     const mockRecommendations = [
//       `Course related to "${input}" 1`,
//       `Course related to "${input}" 2`,
//       `Course related to "${input}" 3`,
//     ];
//     setRecommendations(mockRecommendations);
//   };

//   return (
//     <div className="App">
//       <Header />
//       {/* <Chatbot /> */}
//       <CourseInput onInputSubmit={getRecommendations} />
//       <RecommendationList recommendations={recommendations} />
//     </div>
//   );
// }

const App = () => {
  return (
    <div>
      <Header />
      <Section />
      <Footer />
    </div>
  );
};

export default App;
