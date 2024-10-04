// components/TeamBadge.js
import React from 'react';
// import './TeamBadge.css';
import './../App.css';

const TeamBadge = ({ name, role, image }) => {
  return (
    <div className="badge">
      <img src={image} alt={name} className="badge-avatar" />
      <div className="badge-body">
        <div className="badge-name">{name}</div>
        <div className="badge-role">{role}</div>
        <div className="badge-desc">Lorem ipsum dolor sit amet, consectetur adipiscing elit...</div>
      </div>
    </div>
  );
};

export default TeamBadge;
