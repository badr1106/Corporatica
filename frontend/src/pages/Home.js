import React from "react";
import { motion } from "framer-motion";

const buttonVariants = {
  hover: {
    scale: 1.1,
    textShadow: "0px 0px 8px rgb(255,255,255)",
    boxShadow: "0px 0px 8px rgb(255,255,255)",
  },
  tap: {
    scale: 0.9,
  },
};

const Home = () => {
  return (
    <motion.div
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1>Welcome to the Home Page</h1>
      <motion.button
        variants={buttonVariants}
        whileHover="hover"
        whileTap="tap"
      >
        Test Button
      </motion.button>
    </motion.div>
  );
};

export default Home;
