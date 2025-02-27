from api.index import app

# This is the entry point for Vercel
app.secret_key = app.secret_key or "dev-secret-key"