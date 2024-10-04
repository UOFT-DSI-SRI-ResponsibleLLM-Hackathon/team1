// components/Card.js
import React from 'react';
import './Card.css';

const Card = ({ title, subtitle }) => {
  return (
    <div className="card">
      <div className="card-header"></div>
      <div className="card-body">
        <div className="card-title">{title}</div>
        <div className="card-sub-title">{subtitle}</div>
        <div className="card-desc">Lorem ipsum dolor sit amet, consectetur adipiscing elit...</div>
      </div>
    </div>
  );
};

export default Card;
