import { BrowserRouter, Route, Routes } from "react-router-dom";
import { routes } from "./routes.js";

export function Navigation() {
  return <BrowserRouter><Routes>{routes.map(({ path, layout: Layout, component: Page }) => (
    <Route key={path} path={path} element={<Layout><Page /></Layout>} />
  ))}</Routes></BrowserRouter>;
}
