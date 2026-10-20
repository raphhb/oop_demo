# Deployment Changes

Summary of all changes made to deploy this project to Vercel.

## Files Modified

### `config/settings.py`
- Added `WSGI_APPLICATION = 'config.wsgi.application'` — required by Vercel to locate the Django entrypoint.
- Added `STATIC_ROOT = BASE_DIR / 'staticfiles'` — required for `collectstatic` to run during Vercel build.
- Changed `ALLOWED_HOSTS` to read from the `DJANGO_ALLOWED_HOSTS` environment variable so domains are not hardcoded.

### `shop/templates/shop/index.html`
- Fixed `{% if policy=='regular' %}` → `{% if policy == 'regular' %}` (and same for `student`, `club`) — Django template engine requires spaces around `==`.
- Fixed `{% if not lines %}disabled{%\n endif %}` split across two lines — caused an unclosed tag error.
- Fixed `{{ line.total\n }}` split across two lines — caused the per-line price to render blank in the cart.

## Files Created

### `config/wsgi.py`
- Created the missing WSGI entrypoint. Vercel requires this file to serve the Django app.

### `.gitignore`
- Created to exclude `.venv/`, `staticfiles/`, `__pycache__/`, `*.pyc`, `*.pyo`, `.local-secret`, and `db.sqlite3` from the repository.

## Vercel Environment Variables

Set these in Vercel → Project → Settings → Environment Variables:

| Key | Value |
|---|---|
| `DJANGO_SECRET_KEY` | a long random secret string |
| `DJANGO_ALLOWED_HOSTS` | `oop-demo-gtyg.vercel.app` |
