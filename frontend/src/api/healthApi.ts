// Simple API util for backend health check
export async function fetchHealth() {
  const res = await fetch('/api/health');
  if (!res.ok) throw new Error('Failed to fetch health status');
  return res.json();
}
