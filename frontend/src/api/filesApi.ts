import axios from 'axios';
import { getToken } from './authApi';

const authHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const uploadFile = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data', ...authHeaders() },
    });
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'File upload failed';
  }
};

export const fetchFiles = async () => {
  try {
    const response = await axios.get('/api/files', {
      headers: authHeaders()
    });
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'Fetching files failed';
  }
};

export const previewFile = async (fileId: number) => {
  try {
    const response = await axios.get(`/api/files/${fileId}/preview`, {
      headers: authHeaders()
    });
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'Preview failed';
  }
};

export const deleteFile = async (fileId: number) => {
  try {
    const response = await axios.delete(`/api/files/${fileId}`, {
      headers: authHeaders()
    });
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'File deletion failed';
  }
};
