import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL, // This uses the API URL from your .env file
});

export const getTrashCount = async () => {
  try {
    const response = await api.get('/trash-count');
    return response.data.count;
  } catch (error) {
    console.error('Error fetching trash count:', error);
    throw error;
  }
};

export const getStatus = async () => {
  try {
    const response = await api.get('/status');
    return response.data.status;
  } catch (error) {
    console.error('Error fetching status:', error);
    throw error;
  }
};

export default api;
