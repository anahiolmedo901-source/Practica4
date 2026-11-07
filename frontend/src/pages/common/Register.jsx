import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { registerApi } from "../../api/user.js";
import { useAuth } from "../../hooks/useAuth.js";

export function Register() {
  const { auth } = useAuth();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");
  const formik = useFormik({
    initialValues: { first_name: "", last_name: "", email: "", phone: "", password: "", password_confirm: "" },
    validationSchema: Yup.object({
      first_name: Yup.string().max(150, "Máximo 150 caracteres"),
      last_name: Yup.string().max(150, "Máximo 150 caracteres"),
      email: Yup.string().email("Correo electrónico no válido").required("El correo es obligatorio"),
      phone: Yup.string().max(20, "Máximo 20 caracteres"),
      password: Yup.string().min(8, "Usa al menos 8 caracteres").required("La contraseña es obligatoria"),
      password_confirm: Yup.string().oneOf([Yup.ref("password")], "Las contraseñas no coinciden").required("Confirma tu contraseña"),
    }),
    onSubmit: async ({ password_confirm, ...values }) => {
      setServerError("");
      try {
        await registerApi(values);
        toast.success("Cuenta creada. Ya puedes iniciar sesión.");
        navigate("/login", { replace: true });
      } catch (error) {
        const message = error.message || "No se pudo crear la cuenta.";
        setServerError(message); toast.error(message);
      }
    },
  });
  if (auth) return <Navigate to="/dashboard" replace />;
  const input = (name, label, props = {}) => <Form.Input
    label={label} name={name} value={formik.values[name]}
    onChange={formik.handleChange} onBlur={formik.handleBlur}
    error={formik.touched[name] && formik.errors[name] ? { content: formik.errors[name], pointing: "below" } : false}
    {...props}
  />;
  return <section className="auth-card">
    <p className="eyebrow">Únete a la comunidad</p><h1>Crea tu cuenta</h1>
    <p className="auth-subtitle">Regístrate para consultar tu perfil de Mercado Local.</p>
    <Form onSubmit={formik.handleSubmit}>
      {serverError && <div className="ui error message" role="alert">{serverError}</div>}
      {input("first_name", "Nombre", { autoComplete: "given-name" })}
      {input("last_name", "Apellidos", { autoComplete: "family-name" })}
      {input("email", "Correo electrónico", { type: "email", autoComplete: "email", placeholder: "tu@correo.com" })}
      {input("phone", "Teléfono", { type: "tel", autoComplete: "tel", placeholder: "Opcional" })}
      {input("password", "Contraseña", { type: "password", autoComplete: "new-password" })}
      {input("password_confirm", "Confirma la contraseña", { type: "password", autoComplete: "new-password" })}
      <Button type="submit" primary fluid loading={formik.isSubmitting} disabled={formik.isSubmitting}>Crear cuenta</Button>
    </Form>
    <p className="auth-footnote">¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
  </section>;
}
