// components/Header.js
import React from 'react';
// import './Header.css';
import './../App.css'

const handleStartClick = () => {
  // Scroll the window down by 400 pixels or to a specific element
  window.scrollTo({
    top: window.scrollY + 550,  // Adjust this value to control scroll distance
    behavior: 'smooth',          // Smooth scrolling
  });
};

const Header = () => {
  return (
    <header className="header-banner">
      <div className="container-width">
        <div className="logo-container">
          <div className="logo">Fall 2024</div>
        </div>
        <div className="clearfix"></div>
        <div className="lead-title">GPT Makes Course Selection Easier</div>
        <div className="sub-lead-title">
          Feeling overwhelmed by course selection? <br/>
          Don't worry — we're here to help you navigate your choices with personalized AI recommendations!
        </div>
        <div className="lead-btn" onClick={handleStartClick}>Start!</div>
      </div>
    </header>
  );
};

export default Header;
