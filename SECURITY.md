# Security policy

Mercado Local is an educational project and is not hardened for production use.

## Safe configuration

- Set `DJANGO_SECRET_KEY` outside the repository before running with `DJANGO_DEBUG=false`.
- Set `DJANGO_ALLOWED_HOSTS` to the exact hostnames used by the deployment.
- Serve authenticated endpoints over HTTPS in any hosted environment.
- Do not commit `.env`, `db.sqlite3`, virtual environments, access tokens, or real credentials.

## API safeguards

- User passwords are write-only in the API serializer and are never included in API responses.
- Updating a user without sending `password` preserves the existing password.
- User administration and personal profile endpoints require JWT authentication.

## Reporting a vulnerability

Please report suspected security issues privately through GitHub's repository security advisory feature when it is enabled. Avoid publishing credentials, tokens, or exploit details in a public issue.
