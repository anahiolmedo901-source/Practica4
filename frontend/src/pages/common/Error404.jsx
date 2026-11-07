import { Link } from "react-router-dom";
export function Error404() { return <section className="panel"><h1>Página no encontrada</h1><p>La dirección que buscas no existe.</p><Link to="/">Volver al inicio</Link></section>; }
