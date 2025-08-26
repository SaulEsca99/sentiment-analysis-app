import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sentimentAPI = {
  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },

  analyzeSentiment: async (text, preprocess = true) => {
    try {
      const response = await api.post('/api/analyze', {
        text,
        preprocess,
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      throw error;
    }
  },

  analyzeBatch: async (texts, preprocess = true) => {
    try {
      const response = await api.post('/api/analyze-batch', {
        texts,
        preprocess,
      });
      return response.data;
    } catch (error) {
      console.error('Error in batch analysis:', error);
      throw error;
    }
  },

  getStatistics: async () => {
    try {
      const response = await api.get('/api/stats');
      return response.data;
    } catch (error) {
      console.error('Error getting statistics:', error);
      throw error;
    }
  },

  getModelInfo: async () => {
    try {
      const response = await api.get('/api/model-info');
      return response.data;
    } catch (error) {
      console.error('Error getting model info:', error);
      throw error;
    }
  },
};

export default sentimentAPI;
