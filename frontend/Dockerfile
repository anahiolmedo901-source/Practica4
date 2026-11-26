# Imagen base de Node.js para el frontend React (Vite)
FROM node:22-alpine

WORKDIR /app

# Dependencias de React
COPY package.json package-lock.json ./
RUN npm ci

# Código del frontend
COPY . .

EXPOSE 5173

# --host 0.0.0.0 abre el servidor de Vite a todas las redes; sin esto la
# página se vería en blanco al entrar desde el navegador del equipo anfitrión.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
