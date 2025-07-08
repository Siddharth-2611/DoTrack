from flask import Flask
from app import create_app

app = create_app()

# vercel looks for "app" variable
# This is necessary for the Vercel Python builder to pick it up
