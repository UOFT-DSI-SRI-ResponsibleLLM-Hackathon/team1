// src/components/CourseInput.js
import React, { useState } from 'react';
import './CourseInput.css';
import Card from './Card'; // Import the Card component

function CourseInput({ onInputSubmit }) {
  const [input, setInput] = useState('');

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onInputSubmit(input);
      setInput('');
    }
  };

  return (
    <div className="input-container">
      <form onSubmit={handleSubmit}>
        {/* <Card> */}
            <textarea
                className="course-input"
                value={input}
                onChange={handleInputChange}
                placeholder="Enter course preferences or topics..."
            />
        {/* </Card> */}
            <button type="submit" className="button">
                <div className="blob1"></div>
                <div className="blob2"></div>
                <div className="inner">Get Recommendations</div>
            </button>
        </form>
    </div>
  );
}

export default CourseInput;
