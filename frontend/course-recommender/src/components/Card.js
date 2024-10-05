// components/Card.js
import React from 'react';
import './Card.css';

const Card = ({ title, subtitle, description, link }) => {
  return (
    <a href={link} target="_blank" rel="noopener noreferrer" className="card-link">
      <div className="card">
        <div className="card-header"></div>
        <div className="card-body">
          <div className="card-title">{title}</div>
          <div className="card-sub-title">{subtitle}</div>
          <div className="card-desc">{description}</div>
        </div>
      </div>
    </a>
  );
};

export default Card;
