from flask import Flask, render_template, jsonify, request
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# In-memory storage for subscriptions
subscriptions = {}

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

        # Store subscription in memory
        subscriptions[subscription_id] = {
            'status': 'active',
            'plan': 'premium'
        }

        return jsonify({'success': True, 'message': 'Subscription created successfully'})
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        return jsonify({'success': False, 'message': 'Error processing subscription'}), 500

@app.route('/api/cancel-subscription', methods=['POST'])
def cancel_subscription():
    try:
        data = request.get_json()
        subscription_id = data.get('subscriptionId')
        if subscription_id in subscriptions:
            subscriptions[subscription_id]['status'] = 'cancelled'
            return jsonify({'success': True, 'message': 'Subscription cancelled successfully'})
        else:
            return jsonify({'success': False, 'message': 'Subscription not found'}), 404

    except Exception as e:
        logger.error(f"Error cancelling subscription: {e}")
        return jsonify({'success': False, 'message': 'Error cancelling subscription'}), 500

@app.route('/api/update-payment', methods=['POST'])
def update_payment():
    try:
        # Simplified payment update logic
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
    return render_template('500.html'), 500

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
