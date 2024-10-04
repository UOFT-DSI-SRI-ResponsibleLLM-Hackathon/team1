// src/components/RecommendationList.js
import React from 'react';

function RecommendationList({ recommendations }) {
  return (
    <div style={listContainerStyle}>
      <h2>Recommended Courses:</h2>
      <ul style={listStyle}>
        {recommendations.length > 0 ? (
          recommendations.map((course, index) => (
            <li key={index} style={listItemStyle}>{course}</li>
          ))
        ) : (
          <p>No recommendations available. Try different inputs!</p>
        )}
      </ul>
    </div>
  );
}

const listContainerStyle = {
  textAlign: 'center',
  marginTop: '20px',
};

const listStyle = {
  listStyleType: 'none',
  padding: '0',
};

const listItemStyle = {
  padding: '10px',
  border: '1px solid #ddd',
  margin: '10px 0',
  borderRadius: '5px',
};

export default RecommendationList;
