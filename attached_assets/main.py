from flask import Flask, render_template, redirect, url_for
import os
import logging
import shutil
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///subscription.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.String(255), db.ForeignKey('subscription.subscription_id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

# Ensure static/images directory exists
os.makedirs('static/images', exist_ok=True)

# Copy logo to static directory if it doesn't exist
if not os.path.exists('static/images/PostPilot-logo-text.webp'):
    shutil.copy('attached_assets/PostPilot-logo-text.webp', 'static/images/PostPilot-logo-text.webp')

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # For now, we'll just render a template. Later we can add authentication
    # and actual subscription data
    return render_template('dashboard.html')

@app.route('/payment-history')
def payment_history():
    # For now, we'll just render a template. Later we can add authentication
    # and actual payment data
    return render_template('payment-history.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)