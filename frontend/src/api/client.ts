/**
 * Centralized API base URL configuration.
 *
 * In production (GitHub Pages), VITE_API_BASE_URL is set to the Render backend:
 *   https://autoflow-rag-backend.onrender.com
 *
 * In local development, VITE_API_BASE_URL is left unset (empty string) so that
 * Vite's dev-server proxy (/api → http://127.0.0.1:8000) handles requests,
 * preserving the existing local workflow with no extra configuration.
 *
 * Usage:
 *   import { apiBase } from './client';
 *   fetch(`${apiBase}/api/health`)
 *   axios.get(`${apiBase}/api/files`, ...)
 */
export const apiBase: string = import.meta.env.VITE_API_BASE_URL ?? '';
