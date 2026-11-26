import { routesAdmin } from "./routes.admin.js";
import { routesClient } from "./routes.client.js";
import { routesCommon } from "./routes.common.js";
export const routes = [...routesAdmin, ...routesClient, ...routesCommon];
