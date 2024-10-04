// components/Footer.js
import React from 'react';
// import './Footer.css';
import './../App.css';

const Footer = () => {
  return (
    <footer className="footer-under">
      <div className="container-width">
        <div className="foot-lists">
          {/* Add Footer Lists Here */}
        </div>
        <div className="form-sub">
          <div className="foot-form-cont">
            <div className="foot-form-title">Subscribe</div>
            <input type="text" placeholder="Name" className="sub-input" />
            <input type="text" placeholder="Email" className="sub-input" />
            <button type="button" className="sub-btn">Submit</button>
          </div>
        </div>
      </div>
      <div className="copyright">made with GrapesJS</div>
    </footer>
  );
};

export default Footer;
