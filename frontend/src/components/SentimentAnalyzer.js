// frontend/src/components/SentimentAnalyzer.js
import React, { useState } from 'react';
import sentimentAPI from '../services/api';
import './SentimentAnalyzer.css';

const SentimentAnalyzer = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError('Por favor ingresa un texto para analizar');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await sentimentAPI.analyzeSentiment(text);

      if (response.success) {
        setResult(response.result);
        // Agregar al historial
        setHistory(prev => [response.result, ...prev.slice(0, 4)]);
      } else {
        setError('Error al analizar el texto');
      }
    } catch (err) {
      setError('Error de conexión con el servidor');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    switch(sentiment) {
      case 'POSITIVE': return '#4CAF50';
      case 'NEGATIVE': return '#f44336';
      case 'NEUTRAL': return '#FF9800';
      default: return '#grey';
    }
  };

  const clearAnalysis = () => {
    setText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="sentiment-analyzer">
      <div className="analyzer-container">
        <h2>🎭 Análisis de Sentimientos</h2>

        <div className="input-section">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Escribe o pega aquí el texto que quieres analizar..."
            rows="6"
            maxLength="5000"
            className="text-input"
          />

          <div className="char-counter">
            {text.length} / 5000 caracteres
          </div>

          <div className="button-group">
            <button
              onClick={analyzeSentiment}
              disabled={loading || !text.trim()}
              className="analyze-button"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analizando...
                </>
              ) : (
                <>
                  🔍 Analizar Sentimiento
                </>
              )}
            </button>

            <button
              onClick={clearAnalysis}
              className="clear-button"
            >
              🗑️ Limpiar
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {result && !loading && (
          <div className="result-card" style={{borderColor: getSentimentColor(result.sentiment)}}>
            <div className="result-header">
              <span className="emoji">{result.emoji}</span>
              <div className="sentiment-info">
                <h3>{result.sentiment}</h3>
                <div className="confidence">
                  Confianza: {(result.confidence * 100).toFixed(1)}%
                </div>
              </div>
            </div>

            <div className="metrics">
              <div className="metric-item">
                <label>Estrellas:</label>
                <div className="stars">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={i < result.stars ? 'star filled' : 'star'}>
                      ⭐
                    </span>
                  ))}
                </div>
              </div>

              <div className="metric-item">
                <label>Puntuación:</label>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{
                      width: `${Math.abs(result.sentiment_score) * 100}%`,
                      backgroundColor: getSentimentColor(result.sentiment)
                    }}
                  />
                </div>
              </div>

              <div className="metric-item">
                <label>Tiempo de procesamiento:</label>
                <span>{result.processing_time}s</span>
              </div>
            </div>

            {result.text_truncated && (
              <div className="warning">
                ⚠️ El texto fue truncado a 500 caracteres para el análisis
              </div>
            )}
          </div>
        )}

        {history.length > 0 && (
          <div className="history-section">
            <h3>📊 Historial Reciente</h3>
            <div className="history-list">
              {history.map((item, index) => (
                <div key={index} className="history-item">
                  <span className="history-emoji">{item.emoji}</span>
                  <span className="history-text">
                    {item.text_original.substring(0, 50)}
                    {item.text_original.length > 50 && '...'}
                  </span>
                  <span className="history-sentiment" style={{color: getSentimentColor(item.sentiment)}}>
                    {item.sentiment}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SentimentAnalyzer;