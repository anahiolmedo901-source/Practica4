import { CommonLayout } from "../layouts/index.js";
import { Error404, Login, Register } from "../pages/common/index.js";
export const routesCommon = [
  { path: "/login", layout: CommonLayout, component: Login },
  { path: "/register", layout: CommonLayout, component: Register },
  { path: "*", layout: CommonLayout, component: Error404 },
];
