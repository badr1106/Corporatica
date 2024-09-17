import React, { useState } from 'react';
import axios from 'axios';

function TextAnalysis() {
  const [text, setText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeText = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/api/text/analyze', { text });
      setAnalysis(response.data);
    } catch (error) {
      setError('Error analyzing text: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Text Analysis</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={10}
        cols={50}
      />
      <button onClick={analyzeText} disabled={loading || text.trim().length === 0}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {analysis && (
        <div>
          <h2>Analysis Results</h2>
          <h3>Summary</h3>
          <p>{analysis.summary}</p>
          <h3>Sentiment</h3>
          <p>Label: {analysis.sentiment}</p>
          <p>Score: {analysis.sentiment_score}</p>
        </div>
      )}
    </div>
  );
}

export default TextAnalysis;