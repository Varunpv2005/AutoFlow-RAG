import axios from 'axios';

export const getToken = () => localStorage.getItem('auth_token');

export const setToken = (token: string) => localStorage.setItem('auth_token', token);

export const clearToken = () => {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('auth_username');
};

export const getUsername = () => localStorage.getItem('auth_username');

export const signup = async (username: string, password: string) => {
  const normalizedUsername = username.trim();
  const response = await axios.post('/api/auth/signup', { username: normalizedUsername, password });
  setToken(response.data.access_token);
  localStorage.setItem('auth_username', normalizedUsername);
  return response.data;
};

export const login = async (username: string, password: string) => {
  const normalizedUsername = username.trim();
  const response = await axios.post('/api/auth/login', { username: normalizedUsername, password });
  setToken(response.data.access_token);
  localStorage.setItem('auth_username', normalizedUsername);
  return response.data;
};
