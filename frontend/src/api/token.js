const TOKEN_KEY = import.meta.env.VITE_LOCAL_STORAGE_ITEM_NAME || "MERCADO_LOCAL_ACCESS_TOKEN";
export const getToken = () => window.sessionStorage.getItem(TOKEN_KEY);
export const setToken = (token) => window.sessionStorage.setItem(TOKEN_KEY, token);
export const removeToken = () => window.sessionStorage.removeItem(TOKEN_KEY);
