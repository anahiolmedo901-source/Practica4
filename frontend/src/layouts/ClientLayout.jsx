import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export function ClientLayout({ children }) {
  const { auth, logout } = useAuth();
  return <>
    <header className="site-header">
      <Link className="site-brand" to="/">Mercado Local</Link>
      <nav className="site-nav" aria-label="Navegación principal">
        {auth ? <><Link to="/dashboard">Mi cuenta</Link><button className="ui basic inverted button" onClick={logout}>Cerrar sesión</button></> : <><Link to="/login">Iniciar sesión</Link><Link to="/register">Crear cuenta</Link></>}
      </nav>
    </header>
    <main className="site-main">{children}</main>
  </>;
}
