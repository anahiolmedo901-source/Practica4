import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { loginApi } from "../../api/user.js";
import { useAuth } from "../../hooks/useAuth.js";

export function Login() {
  const { auth, login } = useAuth();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");
  const formik = useFormik({
    initialValues: { email: "", password: "" },
    validationSchema: Yup.object({
      email: Yup.string().email("Correo electrónico no válido").required("El correo es obligatorio"),
      password: Yup.string().required("La contraseña es obligatoria"),
    }),
    onSubmit: async (values) => {
      setServerError("");
      try {
        const { access } = await loginApi(values);
        await login(access);
        navigate("/dashboard", { replace: true });
      } catch (error) {
        const message = error.message || "No se pudo iniciar sesión.";
        setServerError(message); toast.error(message);
      }
    },
  });
  if (auth) return <Navigate to="/dashboard" replace />;
  return <section className="auth-card">
    <p className="eyebrow">Mercado Local</p><h1>Inicia sesión</h1>
    <p className="auth-subtitle">Entra a tu cuenta con el correo que registraste.</p>
    <Form onSubmit={formik.handleSubmit}>
      {serverError && <div className="ui error message" role="alert">{serverError}</div>}
      <Form.Input label="Correo electrónico" name="email" type="email" autoComplete="email" placeholder="tu@correo.com" value={formik.values.email} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.email && formik.errors.email ? { content: formik.errors.email, pointing: "below" } : false} />
      <Form.Input label="Contraseña" name="password" type="password" autoComplete="current-password" placeholder="Tu contraseña" value={formik.values.password} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.password && formik.errors.password ? { content: formik.errors.password, pointing: "below" } : false} />
      <Button type="submit" primary fluid loading={formik.isSubmitting} disabled={formik.isSubmitting}>Iniciar sesión</Button>
    </Form>
    <p className="auth-footnote">¿Aún no tienes cuenta? <Link to="/register">Regístrate</Link></p>
  </section>;
}
