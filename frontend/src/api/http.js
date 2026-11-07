const API_URL = (import.meta.env.VITE_BASE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { Accept: "application/json", ...(options.body ? { "Content-Type": "application/json" } : {}), ...options.headers },
  });
  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    const detail = data?.detail || Object.values(data || {}).flat().join(" ");
    throw new Error(detail || `La solicitud falló (${response.status}).`);
  }
  return data;
}

export const apiRequest = request;
