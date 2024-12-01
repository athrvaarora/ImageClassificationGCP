// frontend/src/components/ImageAnalyzer.jsx
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Upload } from 'lucide-react';

const ImageAnalyzer = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async () => {
    try {
      const response = await fetch('/api/image-analyses');
      const data = await response.json();
      console.log('Fetched analyses:', data); // Debug log
      
      const analysesArray = Object.entries(data)
        .map(([filename, analysis]) => ({
          filename,
          ...analysis
        }))
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      
      setImages(analysesArray);
      if (!selectedImage && analysesArray.length > 0) {
        setSelectedImage(analysesArray[0]);
      }
    } catch (error) {
      console.error('Fetch error:', error);
      setError('Failed to load analyses');
    }
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    setLoading(true);
    try {
      const response = await fetch('/api/classify-image', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) throw new Error('Upload failed');
      
      await fetchAnalyses();
    } catch (error) {
      setError('Failed to upload and analyze image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <label className="flex items-center justify-center w-full p-4 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50">
          <div className="flex flex-col items-center">
            <Upload className="w-8 h-8 mb-2 text-gray-500" />
            <span className="text-sm text-gray-500">Upload image for analysis</span>
          </div>
          <input
            type="file"
            className="hidden"
            accept="image/*"
            onChange={handleImageUpload}
          />
        </label>
      </div>

      {loading && (
        <div className="text-center p-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-2 text-gray-600">Analyzing image...</p>
        </div>
      )}

      {error && (
        <div className="text-red-500 p-4 text-center">{error}</div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="space-y-4">
          {images.map((image) => (
            <div
              key={image.filename}
              onClick={() => setSelectedImage(image)}
              className={`cursor-pointer rounded-lg border-2 p-2 transition-all duration-200 ${
                selectedImage?.filename === image.filename
                  ? 'border-blue-500 shadow-lg'
                  : 'border-transparent hover:border-gray-200'
              }`}
            >
              <img
                src={`/classified_images/${image.filename}`}
                alt={image.filename}
                className="w-full h-40 object-cover rounded"
              />
              <p className="mt-2 text-sm text-gray-600">
                {new Date(image.timestamp).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>

        <div className="md:col-span-2">
          {selectedImage ? (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                <img
                  src={`/classified_images/${selectedImage.filename}`}
                  alt={selectedImage.filename}
                  className="w-full h-auto"
                />
              </div>
              
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="prose prose-sm max-w-none">
                  {selectedImage.classification ? (
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({node, ...props}) => <h1 className="text-2xl font-bold mb-4" {...props} />,
                        h2: ({node, ...props}) => <h2 className="text-xl font-semibold mt-6 mb-3" {...props} />,
                        h3: ({node, ...props}) => <h3 className="text-lg font-medium mt-4 mb-2" {...props} />,
                        p: ({node, ...props}) => <p className="my-2" {...props} />,
                        ul: ({node, ...props}) => <ul className="list-disc ml-4 my-2" {...props} />,
                        li: ({node, ...props}) => <li className="my-1" {...props} />
                      }}
                    >
                      {selectedImage.classification}
                    </ReactMarkdown>
                  ) : (
                    <p className="text-gray-500">No analysis available</p>
                  )}
                </div>
              </div>
              
              <div className="text-sm text-gray-500">
                Analyzed at: {new Date(selectedImage.timestamp).toLocaleString()}
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500">
              Select an image to view its analysis
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageAnalyzer;