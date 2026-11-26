import { Link } from "react-router-dom";

export function Home() {
  return <section className="hero">
    <p className="eyebrow">Del campo y los talleres de la región</p>
    <h1>Encuentra productos locales en un solo lugar.</h1>
    <p>Conoce el catálogo de Mercado Local y crea una cuenta para acceder a tu perfil.</p>
    <Link className="ui primary large button" to="/register">Crear mi cuenta</Link>
  </section>;
}
