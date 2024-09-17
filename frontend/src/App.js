import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { motion } from "framer-motion";
import Home from "./pages/Home";
import TabularData from "./pages/TabularData";
import ImageProcessing from "./pages/ImageProcessing";
import TextAnalysis from "./pages/TextAnalysis";

const pageVariants = {
  initial: {
    opacity: 0,
    y: -50,
  },
  in: {
    opacity: 1,
    y: 0,
  },
  out: {
    opacity: 0,
    y: 50,
  },
};

const pageTransition = {
  type: "tween",
  ease: "anticipate",
  duration: 0.5,
};

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Home />
            </motion.div>
          }
        />
        <Route
          path="/tabular-data"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <TabularData />
            </motion.div>
          }
        />
        <Route
          path="/image-processing"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <ImageProcessing />
            </motion.div>
          }
        />
        <Route
          path="/text-analysis"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <TextAnalysis />
            </motion.div>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
