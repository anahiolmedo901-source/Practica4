import { apiRequest } from "./http.js";

export function loginApi(credentials) {
  return apiRequest("/api/token/", { method: "POST", body: JSON.stringify(credentials) });
}
export function registerApi(formData) {
  return apiRequest("/api/v1/users/", { method: "POST", body: JSON.stringify(formData) });
}
export function getMeApi(token) {
  return apiRequest("/api/v1/me/", { headers: { Authorization: `Bearer ${token}` } });
}
export function getSoapNumberApi(token, number) {
  const query = new URLSearchParams({ numero: String(number) });
  return apiRequest(`/api/v1/soap/numero-a-letras/?${query}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
