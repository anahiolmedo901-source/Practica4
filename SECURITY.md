# Security policy

Mercado Local is an educational project and is not hardened for production use.

## Safe configuration

- Set `DJANGO_SECRET_KEY` outside the repository before running with `DJANGO_DEBUG=false`.
- Set `DJANGO_ALLOWED_HOSTS` to the exact hostnames used by the deployment.
- Serve authenticated endpoints over HTTPS in any hosted environment.
- Do not commit `.env`, `db.sqlite3`, virtual environments, access tokens, or real credentials.
- Configure `CORS_ALLOWED_ORIGINS` with the exact frontend origins; do not enable wildcard CORS for authenticated APIs.

## API safeguards

- User passwords are write-only in the API serializer and are never included in API responses.
- Updating a user without sending `password` preserves the existing password.
- User administration and personal profile endpoints require JWT authentication.
- Full user CRUD is restricted to staff accounts; normal users only see their own profile through `/api/v1/me/`.
- The browser keeps the short-lived access token in `sessionStorage`, which clears it when the tab session ends.
- Registration and password updates use Django's configured password validators.

## Reporting a vulnerability

Please report suspected security issues privately through GitHub's repository security advisory feature when it is enabled. Avoid publishing credentials, tokens, or exploit details in a public issue.
