import { ToastContainer } from "react-toastify";
import { AuthProvider } from "./context/AuthContext.jsx";
import { Navigation } from "./routes/Navigation.jsx";
import "./App.scss";

export default function App() {
  return <AuthProvider><Navigation /><ToastContainer position="bottom-center" autoClose={5000} hideProgressBar newestOnTop closeOnClick pauseOnFocusLoss draggable pauseOnHover /></AuthProvider>;
}
