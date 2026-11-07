import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export function AdminLayout({ children }) {
  const { auth } = useAuth();
  if (auth === undefined) return <div className="loading-page">Cargando sesión…</div>;
  if (!auth) return <Navigate to="/login" replace />;
  return children;
}
