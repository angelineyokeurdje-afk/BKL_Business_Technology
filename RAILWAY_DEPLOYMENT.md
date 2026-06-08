# Railway Deployment Guide for BKLbusiness

This guide ensures your Django application is fully compatible with Railway deployment.

## ✅ Railway Compatibility Status

Your application is now **fully configured** for Railway deployment with the following optimizations:

### Python Version
- **Updated**: `python-3.11.9` (stable, production-ready)
- Replaced: `python-3.14.0` (beta, unstable)

### Database Configuration
- **Secure**: Removed hardcoded credentials from `settings.py`
- **Auto-detection**: `DATABASE_URL` is Railway's standard environment variable
- **Fallback**: Manual database config via env vars if needed

### Secret Key Management
- **Production-safe**: `DJANGO_SECRET_KEY` is now required in production
- **Development**: Safe fallback for local development

### Static Files & Media
- **WhiteNoise**: Configured for serving static files from Railway
- **Cloudinary**: Optional support for image storage on Railway

## 🚀 Deployment Instructions

### 1. Generate a Secure Secret Key

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and save it securely.

### 2. Create Railway Project

```bash
npm install -g @railway/cli
railway login
railway init
```

### 3. Set Required Environment Variables in Railway

In Railway dashboard, set these variables:

**Critical (Required):**
```
DJANGO_SECRET_KEY=<your-secure-key-from-step-1>
DJANGO_DEBUG=false
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=<secure-password>
```

**Optional but Recommended:**
```
DJANGO_ALLOWED_HOSTS=.railway.app
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-specific-password>
```

### 4. Add PostgreSQL Service (Recommended)

In Railway dashboard:
1. Click "Add Service"
2. Select "PostgreSQL"
3. The `DATABASE_URL` will be automatically set

### 5. Deploy

```bash
railway up
```

Or push to your connected GitHub repository and Railway will auto-deploy.

### 6. Verify Deployment

After deployment, visit your Railway URL and:
- Check the homepage loads
- Test login at `/accounts/login/`
- Verify static files load (CSS, JS, images)

## 🔍 Troubleshooting

### Database Connection Error
```
Error: relation does not exist
```
**Solution**: Railway automatically applies migrations during build.sh. Check build logs in Railway dashboard.

### Static Files Not Loading
```
404 on /static/...
```
**Solution**: 
- Ensure `collectstatic` runs in `build.sh` ✓ (already configured)
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py ✓ (already correct)

### Secret Key Error
```
DJANGO_SECRET_KEY environment variable is required in production!
```
**Solution**: Set `DJANGO_SECRET_KEY` in Railway dashboard variables.

### Admin Panel Not Accessible
```
404 at /admin/
```
**Solution**: 
1. Ensure Django admin app is in `INSTALLED_APPS` ✓ (already there)
2. Check migrations ran: `python manage.py showmigrations`

## 📋 File Checklist

- ✅ `runtime.txt` - Python 3.11.9 (stable)
- ✅ `requirements.txt` - All dependencies listed
- ✅ `railway.json` - Deployment configuration
- ✅ `Procfile` - Process definition
- ✅ `build.sh` - Build commands (migrations, collectstatic, superuser)
- ✅ `bklbusiness/settings.py` - Production-safe configuration
- ✅ `bklbusiness/wsgi.py` - WSGI application
- ✅ `.env.example` - Environment variables template
- ✅ `.gitignore` - Proper ignore patterns

## 🔒 Security Best Practices

✅ **Implemented:**
- HTTPS enforcement in production (`SECURE_SSL_REDIRECT`)
- Secure session cookies (`SESSION_COOKIE_SECURE`)
- CSRF protection (`CSRF_COOKIE_SECURE`)
- HSTS headers (`SECURE_HSTS_SECONDS`)
- XFrame protection (`X_FRAME_OPTIONS = 'DENY'`)
- Content type protection (`SECURE_CONTENT_TYPE_NOSNIFF`)
- XSS filter (`SECURE_BROWSER_XSS_FILTER`)

⚠️ **To Enable:**
- Add `DJANGO_SECRET_KEY` in Railway variables
- Use strong password for `DJANGO_SUPERUSER_PASSWORD`
- Configure proper email credentials for password reset

## 📞 Support Resources

- [Railway Docs](https://docs.railway.app)
- [Django Deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Gunicorn Docs](https://docs.gunicorn.org/)

## 🎉 Next Steps

1. Ensure PostgreSQL service is added to Railway
2. Set all required environment variables
3. Deploy with `railway up` or push to GitHub
4. Monitor logs: `railway logs`
5. Test the application thoroughly

Your application is now **production-ready for Railway**!
