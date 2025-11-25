# Heroku Deployment & Database Migration Guide

## What Just Happened?

When you push code changes to GitHub that include database model changes (like adding the `date_of_birth` field to the UserProfile model), Django creates migration files locally. However, these migrations don't automatically run on your Heroku production database. This causes a **Server Error (500)** because the application code expects database fields that don't exist yet.

### The Problem
- Local development had the new `date_of_birth` field
- Heroku production database didn't have this field
- Application crashed when trying to access user profiles

### The Solution
We used the Heroku CLI to run the pending database migrations on your production server, adding the missing field and updating the database schema.

---

## How to Deploy Database Changes to Heroku in the Future

### Step 1: Make Changes Locally
1. Modify your Django models (e.g., `users/models.py`)
2. Create migrations locally:
   ```bash
   python manage.py makemigrations
   ```
3. Test migrations locally:
   ```bash
   python manage.py migrate
   ```
4. Test your application locally to ensure everything works

### Step 2: Commit and Push to GitHub
```bash
git add .
git commit -m "Add new feature with database changes"
git push origin main
```

### Step 3: Deploy to Heroku
Heroku automatically deploys when you push to GitHub (if auto-deploy is enabled in your Heroku dashboard).

### Step 4: Run Migrations on Heroku
**This is the critical step that must be done manually:**

```bash
heroku run python manage.py migrate --app getlizzyfit
```

**Why this step is necessary:**
- Heroku deploys your code automatically
- But it does NOT automatically run database migrations
- You must manually trigger migrations using the Heroku CLI

---

## Heroku CLI Setup (One-Time)

### Installation
1. Download from: https://devcenter.heroku.com/articles/heroku-cli
2. Install the Heroku CLI
3. Restart your terminal

### Login (First Time Only)
```bash
heroku login
```
This opens a browser window for authentication.

### Finding Your App Name
```bash
heroku apps
```
Your app is: **getlizzyfit**

---

## Common Heroku Commands

### Check if your app is running
```bash
heroku ps --app getlizzyfit
```

### View logs (for debugging)
```bash
heroku logs --tail --app getlizzyfit
```

### Run migrations
```bash
heroku run python manage.py migrate --app getlizzyfit
```

### Create a superuser on Heroku
```bash
heroku run python manage.py createsuperuser --app getlizzyfit
```

### Check database status
```bash
heroku run python manage.py showmigrations --app getlizzyfit
```

### Access Python shell on Heroku
```bash
heroku run python manage.py shell --app getlizzyfit
```

### Restart the application
```bash
heroku restart --app getlizzyfit
```

---

## Windows-Specific Heroku CLI Usage

If `heroku` command isn't found in your terminal, use the full path:

```bash
"/c/Program Files/heroku/bin/heroku" run python manage.py migrate --app getlizzyfit
```

You may need to add Heroku to your PATH environment variable for the command to work without the full path.

---

## Typical Deployment Workflow

1. **Develop locally** - Make code changes and test
2. **Create migrations** - `python manage.py makemigrations`
3. **Test migrations** - `python manage.py migrate`
4. **Commit changes** - `git add . && git commit -m "Description"`
5. **Push to GitHub** - `git push origin main`
6. **Wait for Heroku deploy** - Check Heroku dashboard or logs
7. **Run migrations on Heroku** - `heroku run python manage.py migrate --app getlizzyfit`
8. **Test production site** - Visit your Heroku URL

---

## Troubleshooting

### 500 Server Error After Deployment
**Cause:** Database migrations not run on Heroku
**Solution:** 
```bash
heroku run python manage.py migrate --app getlizzyfit
```

### Changes Not Appearing on Heroku
**Cause:** Code might not have deployed
**Solution:** Check deployment logs in Heroku dashboard or force a rebuild

### Database Connection Issues
**Solution:** Check your Heroku Postgres add-on status in the dashboard

### Static Files Not Loading
**Solution:**
```bash
heroku run python manage.py collectstatic --noinput --app getlizzyfit
```

---

## Important Notes

⚠️ **Always run migrations after deploying model changes**
- Model changes = migrations needed
- Forms, views, templates usually don't need migrations
- When in doubt, check: `heroku run python manage.py showmigrations --app getlizzyfit`

✅ **Best Practice:**
- Test everything locally first
- Keep migrations small and focused
- Always backup your production database before major schema changes
- Review migration files before committing them

🔒 **Security:**
- Never commit `.env` files with secrets
- Use Heroku Config Vars for sensitive data (accessible in Heroku dashboard under Settings)
- Keep `DEBUG = False` in production (already configured in your settings.py)

---

## Quick Reference Card

```bash
# Login to Heroku
heroku login

# List your apps
heroku apps

# Run migrations
heroku run python manage.py migrate --app getlizzyfit

# View logs
heroku logs --tail --app getlizzyfit

# Check migration status
heroku run python manage.py showmigrations --app getlizzyfit

# Restart app
heroku restart --app getlizzyfit
```

---

## Additional Resources

- [Heroku Django Documentation](https://devcenter.heroku.com/articles/django-app-configuration)
- [Heroku CLI Documentation](https://devcenter.heroku.com/articles/heroku-cli)
- [Django Migrations Guide](https://docs.djangoproject.com/en/stable/topics/migrations/)
