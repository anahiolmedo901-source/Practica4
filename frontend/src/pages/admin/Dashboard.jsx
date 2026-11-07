import { Button } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth.js";

export function Dashboard() {
  const { auth, logout } = useAuth();
  const user = auth.me;
  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ") || "Cliente de Mercado Local";
  return <section className="panel">
    <p className="eyebrow">Tu cuenta</p>
    <h1>Bienvenido, {fullName}</h1>
    <p>Estos son los datos personales vinculados con tu sesión.</p>
    <div className="profile-grid">
      <div className="profile-item"><span>Correo electrónico</span><strong>{user.email}</strong></div>
      <div className="profile-item"><span>Teléfono</span><strong>{user.phone || "No registrado"}</strong></div>
    </div>
    <Button onClick={logout}>Cerrar sesión</Button>
  </section>;
}
