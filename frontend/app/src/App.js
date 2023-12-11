// App.js
import React, { useState, useEffect } from 'react';
import Sidebar from "./components/Sidebar/Sidebar";
import Layout from './components/Layout/Layout';
import api from './api';

const App = () => {
  const [apiResult, setApiResult] = useState(null);

  const fetchTest = async () => {
    try {
      const response = await api.get("/");
      return response.data; // Assuming the data you want to render is in the response body
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error; // Handle the error or propagate it as needed
    }
  };

  useEffect(() => {
    const testApiConnection = async () => {
      try {
        const result = await fetchTest();
        setApiResult(result);
      } catch (error) {
        // Handle errors if needed
      }
    };

    testApiConnection();
  }, []); // Empty dependency array ensures the effect runs only once on mount

  return (
    <>
      {/* <Layout /> */}
      <div>
        {/* Render the API result */}
        {apiResult !== null ? (
          <p>API Result: {apiResult}</p>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </>
  );
};

export default App;
