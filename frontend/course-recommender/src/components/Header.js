// src/components/Header.js
// import React from 'react';

// function Header() {
//   return (
//     <header style={headerStyle}>
//       <h1>Course Recommender</h1>
//       <p>Get personalized course recommendations based on your interests!</p>
//     </header>
//   );
// }

// const headerStyle = {
//   backgroundColor: '#282c34',
//   color: 'white',
//   padding: '10px',
//   textAlign: 'center',
// };

// components/Header.js
import React from 'react';
// import './Header.css';
import './../App.css'

const Header = () => {
  return (
    <header className="header-banner">
      <div className="container-width">
        <div className="logo-container">
          <div className="logo">Fall 2024</div>
        </div>
        {/* <nav className="menu">
          <div className="menu-item">Builder</div>
          <div className="menu-item">TEMPLATE</div>
          <div className="menu-item">WEB</div>
        </nav> */}
        <div className="clearfix"></div>
        <div className="lead-title">GPT Makes Course Selection Easier</div>
        <div className="sub-lead-title">
          Feeling overwhelmed by course selection? <br/>
          Don't worry — we're here to help you navigate your choices with personalized AI recommendations!
        </div>
        <div className="lead-btn">Start!</div>
      </div>
    </header>
  );
};

export default Header;
