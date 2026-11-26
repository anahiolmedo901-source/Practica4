import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { getMeApi } from "../api/user.js";
import { getToken, removeToken, setToken } from "../api/token.js";

export const AuthContext = createContext({ auth: undefined, login: async () => {}, logout: () => {} });

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const login = useCallback(async (accessToken) => {
    setToken(accessToken);
    try {
      const me = await getMeApi(accessToken);
      setAuth({ token: accessToken, me });
      return me;
    } catch (error) {
      removeToken(); setAuth(null); throw error;
    }
  }, []);
  const logout = useCallback(() => { removeToken(); setAuth(null); }, []);
  useEffect(() => {
    let active = true;
    const token = getToken();
    if (!token) setAuth(null);
    else getMeApi(token)
      .then((me) => { if (active) setAuth({ token, me }); })
      .catch(() => { removeToken(); if (active) setAuth(null); });
    return () => { active = false; };
  }, []);
  const value = useMemo(() => ({ auth, login, logout }), [auth, login, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
