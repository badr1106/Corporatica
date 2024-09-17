import React, { useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function ImageProcessing() {
  const [image, setImage] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = (event) => {
    setImage(event.target.files[0]);
  };

  const analyzeImage = async () => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await axios.post('http://localhost:8000/api/image/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setAnalysis(response.data);
    } catch (error) {
      setError('Error analyzing image: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Image Processing</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      <button onClick={analyzeImage} disabled={loading || !image}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {analysis && (
        <div>
          <h2>Analysis Results</h2>
          <h3>Color Histogram</h3>
          <BarChart width={600} height={300} data={analysis.histogram.map((value, index) => ({ bin: index, value }))}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="bin" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
          <h3>Segmented Image</h3>
          <img src={`data:image/png;base64,${analysis.segmented_image}`} alt="Segmented" />
        </div>
      )}
    </div>
  );
}

export default ImageProcessing;