from flask import Flask, render_template, redirect, url_for, jsonify, request
import os
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure SQLAlchemy with connection pooling for serverless
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 1,
    'pool_timeout': 30,
    'pool_recycle': 1800,
    'pool_pre_ping': True
}

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/payment-history')
def payment_history():
    return render_template('payment-history.html')

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        subscription_id = data.get('subscriptionId')

        if not subscription_id:
            return jsonify({'success': False, 'message': 'Subscription ID is required'}), 400

        subscription = Subscription(
            subscription_id=subscription_id,
            status='active'
        )
        db.session.add(subscription)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Subscription created successfully'})
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        return jsonify({'success': False, 'message': 'Error processing subscription'}), 500

@app.route('/api/cancel-subscription', methods=['POST'])
def cancel_subscription():
    try:
        # Implement subscription cancellation logic here
        return jsonify({'success': True, 'message': 'Subscription cancelled successfully'})
    except Exception as e:
        logger.error(f"Error cancelling subscription: {e}")
        return jsonify({'success': False, 'message': 'Error cancelling subscription'}), 500

@app.route('/api/update-payment', methods=['POST'])
def update_payment():
    try:
        # Implement payment update logic here
        return jsonify({'success': True, 'url': '/update-payment'})
    except Exception as e:
        logger.error(f"Error updating payment method: {e}")
        return jsonify({'success': False, 'message': 'Error updating payment method'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize database
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)