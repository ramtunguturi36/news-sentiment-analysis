from app import app as application

# This file is required for Vercel to recognize the WSGI application
# The variable `app` is referenced as `application` here so Vercel can import it
app = application
