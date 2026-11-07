# Mercado Local API

Aplicación de Mercado Local con Django REST Framework y React. Incluye cuentas con inicio por correo electrónico, JWT, perfil protegido, productos de muestra de una API de terceros, consumo SOAP desde Django y Swagger.

## Preparación local

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

En otra terminal, inicia el cliente React:

```powershell
cd frontend
npm install
npm run dev
```

El cliente abre en `http://localhost:5173`. El backend permite CORS solo desde
ese origen (y `127.0.0.1:5173`) de forma predeterminada. Si usas otro origen,
configúralo explícitamente en `CORS_ALLOWED_ORIGINS`.

La base de desarrollo es SQLite. El archivo `db.sqlite3` y el entorno virtual se excluyen de Git.
En desarrollo se genera una clave local temporal. Para ejecutar fuera de desarrollo, define `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false` y `DJANGO_ALLOWED_HOSTS` en el entorno; no guardes secretos en el repositorio.
Consulta [SECURITY.md](SECURITY.md) para las prácticas de configuración y reporte de vulnerabilidades.

## Rutas principales

- Swagger: `http://127.0.0.1:8000/swagger/`
- Crear usuario: `POST /api/v1/users/`
- CRUD de usuarios: `/api/v1/users/` (registro público; administración solo para staff con JWT)
- Datos del usuario autenticado: `GET /api/v1/me/`
- Obtener token: `POST /api/token/` con `email` y `password`
- Renovar token: `POST /api/token/refresh/`
- Consumo SOAP desde Django: `GET /api/v1/soap/numero-a-letras/?numero=42` (requiere JWT)
- Administración: `/admin/`
- Cliente React: `http://localhost:5173/` (inicio), `/login`, `/register` y `/dashboard`

El token de acceso vence en 15 minutos. El campo `password` solo acepta escritura y nunca se incluye en respuestas. Al editar un usuario sin enviar contraseña, la contraseña existente se conserva.

El frontend obtiene el JWT desde `/api/token/`, conserva únicamente el token de
acceso durante la sesión del navegador y carga el perfil desde `/api/v1/me/`.
El formulario de registro usa `/api/v1/users/`; no muestra ni registra
contraseñas en la interfaz.

El dashboard autenticado muestra el nombre del usuario, productos de muestra de
DummyJSON y el resultado de la conversión `42` del servicio NumberConversion
SOAP consumido por Django. Para probar el SOAP directamente desde PowerShell,
inicia sesión de forma interactiva y consulta la ruta protegida:

```powershell
$email = Read-Host 'Correo registrado'
$securePassword = Read-Host 'Contraseña' -AsSecureString
$password = [Net.NetworkCredential]::new('', $securePassword).Password
$body = @{ email = $email; password = $password } | ConvertTo-Json
$jwt = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/api/token/' -ContentType 'application/json' -Body $body
$result = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/soap/numero-a-letras/?numero=42' -Headers @{ Authorization = "Bearer $($jwt.access)" }
$result | ConvertTo-Json
Remove-Variable password, securePassword, jwt
```

Toma estas cuatro capturas: (1) login con la consola abierta; (2) dashboard
protegido mostrando el nombre; (3) widget con productos externos ya cargados;
(4) terminal con la respuesta JSON del endpoint Django SOAP. Para la captura 1,
abre las herramientas de desarrollador (F12), pestaña Console, antes de iniciar
sesión: aparecerá el mensaje de éxito, nunca el valor del token. El endpoint
SOAP autenticado también está documentado en Swagger. Se requiere conexión a
Internet para DummyJSON y DataAccess SOAP.

## Publicación en GitHub

El proyecto se entrega en la rama `dev` de `https://github.com/anahiolmedo901-source/Practica4`. Para publicarlo desde una copia local:

```powershell
git remote set-url origin https://github.com/anahiolmedo901-source/Practica4.git
git switch -c dev
git push -u origin dev
```
