import { Button } from "semantic-ui-react";
import { useEffect, useState } from "react";
import { getExternalProducts } from "../../api/external.js";
import { getSoapNumberApi } from "../../api/user.js";
import { useAuth } from "../../hooks/useAuth.js";

export function Dashboard() {
  const { auth, logout } = useAuth();
  const user = auth.me;
  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ") || "Cliente de Mercado Local";
  const [products, setProducts] = useState([]);
  const [productsError, setProductsError] = useState("");
  const [soapResult, setSoapResult] = useState(null);
  const [soapError, setSoapError] = useState("");

  useEffect(() => {
    let active = true;
    getExternalProducts()
      .then((items) => { if (active) setProducts(items); })
      .catch(() => { if (active) setProductsError("No fue posible cargar los productos de la API externa."); });
    getSoapNumberApi(auth.token, 42)
      .then((result) => { if (active) setSoapResult(result); })
      .catch((error) => { if (active) setSoapError(error.message || "No fue posible consultar el servicio SOAP."); });
    return () => { active = false; };
  }, [auth.token]);

  return <section className="panel">
    <p className="eyebrow">Tu cuenta</p>
    <h1>Bienvenido, {fullName}</h1>
    <p>Estos son los datos personales vinculados con tu sesión.</p>
    <div className="profile-grid">
      <div className="profile-item"><span>Correo electrónico</span><strong>{user.email}</strong></div>
      <div className="profile-item"><span>Teléfono</span><strong>{user.phone || "No registrado"}</strong></div>
    </div>
    <section className="dashboard-widget" aria-labelledby="third-party-title">
      <p className="eyebrow">API de terceros · DummyJSON</p>
      <h2 id="third-party-title">Productos de muestra</h2>
      {productsError ? <p role="status">{productsError}</p> : products.length === 0 ? <p role="status">Cargando datos externos…</p> :
        <div className="product-grid">{products.map((product) => <article className="external-product" key={product.id}>
          <img src={product.thumbnail} alt="" loading="lazy" />
          <div><strong>{product.title}</strong><span>{product.category}</span><b>{new Intl.NumberFormat("es-MX", { style: "currency", currency: "USD" }).format(product.price)}</b></div>
        </article>)}</div>}
    </section>
    <section className="dashboard-widget soap-widget" aria-labelledby="soap-title">
      <p className="eyebrow">Django → servicio SOAP</p>
      <h2 id="soap-title">Conversión de ejemplo</h2>
      {soapError ? <p role="status">{soapError}</p> : soapResult ? <p className="soap-result"><strong>{soapResult.numero}</strong><span>{soapResult.resultado}</span></p> : <p role="status">Consultando el servicio SOAP…</p>}
      <small>Respuesta de NumberConversion SOAP recibida por el backend Django.</small>
    </section>
    <Button onClick={logout}>Cerrar sesión</Button>
  </section>;
}
