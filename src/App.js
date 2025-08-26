import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SentimentAnalyzer from './components/SentimentAnalyzer';
import BatchAnalyzer from './components/BatchAnalyzer';
import Statistics from './components/Statistics';
import LoadingSpinner from './components/LoadingSpinner';
import { sentimentAPI } from './services/api';
import './styles/App.css';

function App() {
  const [loading, setLoading] = useState(true);
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await sentimentAPI.getHealth();
      setBackendStatus('online');
    } catch (error) {
      setBackendStatus('offline');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Checking backend connection..." />;
  }

  if (backendStatus === 'offline') {
    return (
      <div className="app-error">
        <h2>⚠️ Backend Server Offline</h2>
        <p>Please make sure the Flask server is running on port 5000</p>
        <p>Run: <code>python src/main.py</code> in your backend directory</p>
      </div>
    );
  }

  return (
    <div className="App">
      <Header />
      <div className="container">
        <div className="dashboard">
          <SentimentAnalyzer />
          <BatchAnalyzer />
          <Statistics />
        </div>
      </div>
    </div>
  );
}

export default App;
