import React, { useState, useEffect } from 'react';
import SentimentAnalyzer from './components/SentimentAnalyzer';
import sentimentAPI from './services/api';
import './App.css';

function App() {
  const [serverStatus, setServerStatus] = useState('checking');
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    checkServerStatus();
  }, []);

  const checkServerStatus = async () => {
    try {
      const health = await sentimentAPI.checkHealth();
      const info = await sentimentAPI.getModelInfo();
      
      if (health.status === 'healthy') {
        setServerStatus('online');
        setModelInfo(info);
      } else {
        setServerStatus('offline');
      }
    } catch (error) {
      console.error('Error checking server:', error);
      setServerStatus('offline');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎭 Sistema de Análisis de Sentimientos</h1>
        <p>Desarrollado por Saúl Escamilla Lazcano</p>
        
        <div className="status-bar">
          <span className={`status-indicator ${serverStatus}`}>
            {serverStatus === 'online' ? '🟢' : '🔴'}
          </span>
          <span>
            Servidor: {serverStatus === 'online' ? 'En línea' : 'Fuera de línea'}
          </span>
          {modelInfo && (
            <span className="model-info">
              | Modelo: {modelInfo.model_name}
            </span>
          )}
        </div>
      </header>

      <main>
        {serverStatus === 'online' ? (
          <SentimentAnalyzer />
        ) : serverStatus === 'offline' ? (
          <div className="error-container">
            <h2>⚠️ Servidor no disponible</h2>
            <p>Asegúrate de que el servidor esté corriendo en http://localhost:5000</p>
            <button onClick={checkServerStatus}>Reintentar</button>
          </div>
        ) : (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Conectando con el servidor...</p>
          </div>
        )}
      </main>

      <footer>
        <p>© 2025 - Proyecto de IA y NLP | IPN - ESCOM</p>
        <p>
          <a href="https://github.com/tu-usuario/sentiment-analysis-app" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
          {' | '}
          <a href="http://localhost:5000" target="_blank" rel="noopener noreferrer">
            API Docs
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;