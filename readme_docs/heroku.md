# Deployment, Testing & Known Bugs Documentation

## Deployment to Heroku

This project was successfully deployed to **Heroku** using the official Python buildpack. The deployment process required resolving multiple structural and configuration issues common to Django applications hosted on Heroku.

The final deployed application runs correctly using Gunicorn and is accessible via its public Heroku URL.

---

## Deployment Process

### 1. Version Control & Environment

- The project is version-controlled using Git and hosted on GitHub
- A Heroku app was created and linked via a Heroku Git remote
- Sensitive configuration values were handled using environment variables

Local development used a `.env` file, which was **excluded from version control**.

---

### 2. Python Buildpack Detection

#### Issue
Heroku initially failed to detect the Python app and rejected deployment.

#### Cause
The `requirements.txt` file was not located in the project root directory, preventing Heroku from detecting the Python buildpack.

#### Resolution
- Moved `requirements.txt` to the repository root
- Ensured it was tracked by Git

After this change, Heroku successfully detected the Python application and installed dependencies.

---

### 3. Gunicorn & WSGI Configuration

#### Issue
Gunicorn failed to boot with repeated module import errors, including:

```
ModuleNotFoundError: No module named 'bubblebubble.wsgi'
ModuleNotFoundError: No module named 'bubblebubble.bubblebubble'
```

#### Cause
The Django project follows the standard nested structure:

```
bubblebubble/            (project root)
└── bubblebubble/        (Django package)
    ├── settings.py
    ├── wsgi.py
```

Heroku runs the application from `/app`, which caused Python to resolve imports incorrectly when Gunicorn was launched from the root.

#### Resolution
The `Procfile` was updated to explicitly change directory into the Django project folder before starting Gunicorn.

**Final `Procfile`:**
```procfile
web: gunicorn --chdir bubblebubble bubblebubble.wsgi
```

This ensured that:
- Python imports resolved correctly
- Django settings and WSGI loaded without error
- No manual `PYTHONPATH` configuration was required

---

### 4. Environment Variable Configuration

The following Heroku config variables were set:

- `DJANGO_SETTINGS_MODULE = bubblebubble.settings`
- `SECRET_KEY = <secure value>`

A previously added `PYTHONPATH` variable was removed after it was found to interfere with Django's import resolution.

---

### 5. Template Resolution Fix

#### Issue
After successful deployment, the application returned a 500 error:

```
TemplateDoesNotExist: base.html
```

#### Cause
Django was not aware of the global templates directory.

#### Resolution
The `TEMPLATES` setting in `settings.py` was updated:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

This allowed Django to locate `base.html` and render templates correctly.

---

## Testing

### Manual Testing

The application was manually tested in both **local development** and **production (Heroku)** environments.

| Feature | Result |
|------|------|
| Homepage loads correctly | Pass |
| Template inheritance works | Pass |
| Static assets load | Pass |
| Django admin accessible | Pass |
| No runtime errors in logs | Pass |

Heroku logs were monitored using:
```bash
heroku logs --tail
```

No critical errors were observed after final deployment.

---

## Known Bugs

### 1. Django Admin Styling (Heroku)

**Issue:**
Occasionally, Django admin styling may not load fully in the Heroku environment.

**Cause:**
Static files are not currently collected and served via a dedicated static file handler.

**Status:**
Resolved

**Fix:**
- Configure `collectstatic`
- Add WhiteNoise or a cloud-based static file service

---

### 2. Favicon 404 Error

**Issue:**
Requests to `/favicon.ico` return a 404 error.

**Cause:**
No favicon file has been added to the static assets.

**Status:**
Resolved

**Fix:**
Add a favicon file and configure static paths.

---

### 3. No Custom Error Pages

**Issue:**
Default Django error pages are shown for 404 and 500 errors.

**Status:**
Resolved

**Fix:**
Create custom `404.html` and `500.html` templates.

---

## Conclusion

The project is fully deployed and operational on Heroku. The deployment process required resolving several non-trivial issues related to Django structure, Gunicorn configuration, and Heroku buildpack expectations.

All core functionality works as intended, and remaining issues are minor and clearly documented for future improvement.

