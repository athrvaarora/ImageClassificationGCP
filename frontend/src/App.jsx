import React from 'react';
import Navigation from './components/Navigation';
import ImageAnalyzer from './components/ImageAnalyzer';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      <main className="max-w-7xl mx-auto py-6 px-6">
        <ImageAnalyzer />
      </main>
    </div>
  );
};

export default App;