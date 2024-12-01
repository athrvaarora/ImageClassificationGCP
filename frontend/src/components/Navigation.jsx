// frontend/src/components/Navigation.jsx
import React from 'react';

const Navigation = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <span className="text-xl font-bold text-gray-800">ImageInsight</span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;