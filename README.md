# Mercado Local API

API REST desarrollada con Django y Django REST Framework para el catálogo de una tienda de productos locales. Incluye cuentas con inicio por correo electrónico, CRUD protegido de usuarios, consulta del perfil autenticado, JWT y Swagger.

## Preparación local

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La base de desarrollo es SQLite. El archivo `db.sqlite3` y el entorno virtual se excluyen de Git.
En desarrollo se genera una clave local temporal. Para ejecutar fuera de desarrollo, define `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false` y `DJANGO_ALLOWED_HOSTS` en el entorno; no guardes secretos en el repositorio.
Consulta [SECURITY.md](SECURITY.md) para las prácticas de configuración y reporte de vulnerabilidades.

## Rutas principales

- Swagger: `http://127.0.0.1:8000/swagger/`
- Crear usuario: `POST /api/v1/users/`
- CRUD de usuarios: `/api/v1/users/` (las operaciones distintas al registro requieren JWT)
- Datos del usuario autenticado: `GET /api/v1/me/`
- Obtener token: `POST /api/token/` con `email` y `password`
- Renovar token: `POST /api/token/refresh/`
- Administración: `/admin/`

El token de acceso vence en 15 minutos. El campo `password` solo acepta escritura y nunca se incluye en respuestas. Al editar un usuario sin enviar contraseña, la contraseña existente se conserva.

## Publicación en GitHub

El proyecto se entrega en la rama `dev` de `https://github.com/anahiolmedo901-source/Practica4`. Para publicarlo desde una copia local:

```powershell
git remote set-url origin https://github.com/anahiolmedo901-source/Practica4.git
git switch -c dev
git push -u origin dev
```
