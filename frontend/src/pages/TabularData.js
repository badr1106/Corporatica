import React, { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Brush,
  ResponsiveContainer,
} from "recharts";

const TabularData = () => {
  const [data, setData] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const rows = text.split("\n").map((row) => row.split(","));
      const headers = rows[0];
      const dataRows = rows.slice(1).map((row) => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = parseFloat(row[index]);
        });
        return obj;
      });
      setData(dataRows);
    };
    reader.readAsText(file);
  };

  const analyzeData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/tabular/analyze",
        { data }
      );
      setAnalysis(response.data);
    } catch (error) {
      setError("Error analyzing data: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1>Tabular Data Analysis</h1>
      <input type="file" onChange={handleFileUpload} />
      <motion.button
        onClick={analyzeData}
        disabled={loading || data.length === 0}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </motion.button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{
            duration: 0.5,
            repeat: Infinity,
            repeatType: "reverse",
          }}
        >
          Loading...
        </motion.div>
      )}
      {analysis && (
        <div>
          <h2>Analysis Results</h2>
          <pre>{JSON.stringify(analysis, null, 2)}</pre>
          <h2>Data Visualization</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Brush dataKey="name" height={30} stroke="#8884d8" />
              {Object.keys(data[0] || {}).map((key, index) => (
                <Line
                  key={index}
                  type="monotone"
                  dataKey={key}
                  stroke={`#${Math.floor(Math.random() * 16777215).toString(
                    16
                  )}`}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </motion.div>
  );
};

export default TabularData;
