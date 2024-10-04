// components/PriceCard.js
import React from 'react';
// import './PriceCard.css';
import './../App.css';

const PriceCard = ({ title, description, price }) => {
  return (
    <div className="price-card-cont">
      <div className="price-card">
        <div className="pc-title">{title}</div>
        <div className="pc-desc">{description}</div>
        <div className="pc-amount">{price}</div>
      </div>
    </div>
  );
};

export default PriceCard;
