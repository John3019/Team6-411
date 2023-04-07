import React from 'react';

const Slider = ({ items }) => {
  return (
    <div className="slider">
      {items.map((item, index) => (
        <div key={index} className="slider-item">
          {item}
        </div>
      ))}
    </div>
  );
};

export default Slider;
