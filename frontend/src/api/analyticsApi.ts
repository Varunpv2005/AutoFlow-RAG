import axios from 'axios';
import { apiBase } from './client';
import { getToken } from './authApi';

const authHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const fetchAnalytics = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/analytics`, {
      headers: authHeaders()
    });
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'Fetching analytics failed';
  }
};
