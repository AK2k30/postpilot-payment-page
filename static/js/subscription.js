// PayPal subscription handling
if (typeof paypal !== 'undefined') {
    paypal.Buttons({
        createSubscription: function(data, actions) {
            return actions.subscription.create({
                'plan_id': 'P-9U345022LR302184VM67SLCA'
            });
        },
        onApprove: function(data, actions) {
            showLoadingOverlay();
            // Handle successful subscription
            fetch('/api/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    subscriptionId: data.subscriptionID
                })
            })
            .then(response => response.json())
            .then(data => {
                hideLoadingOverlay();
                if (data.success) {
                    showSuccessAlert();
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 2000);
                } else {
                    showErrorAlert(data.message || 'Subscription error occurred');
                }
            })
            .catch(error => {
                hideLoadingOverlay();
                showErrorAlert('Error processing subscription');
                console.error('Error:', error);
            });
        },
        onError: function(err) {
            hideLoadingOverlay();
            showErrorAlert('PayPal error occurred');
            console.error('PayPal Error:', err);
        }
    }).render('#paypal-button-container-P-9U345022LR302184VM67SLCA');
}

// UI Helper Functions
function showLoadingOverlay() {
    document.getElementById('loading-overlay').classList.remove('d-none');
}

function hideLoadingOverlay() {
    document.getElementById('loading-overlay').classList.add('d-none');
}

function showSuccessAlert() {
    const alert = document.getElementById('success-alert');
    alert.classList.remove('d-none');
    setTimeout(() => {
        alert.classList.add('d-none');
    }, 5000);
}

function showErrorAlert(message) {
    const alert = document.getElementById('error-alert');
    const messageElement = document.getElementById('error-message');
    messageElement.textContent = message;
    alert.classList.remove('d-none');
    setTimeout(() => {
        alert.classList.add('d-none');
    }, 5000);
}

// Dashboard functions
function cancelSubscription() {
    if (confirm('Are you sure you want to cancel your subscription? This will take effect at the end of your current billing period.')) {
        showLoadingOverlay();
        fetch('/api/cancel-subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingOverlay();
            if (data.success) {
                alert('Subscription cancelled successfully. Changes will take effect at the end of your billing period.');
                location.reload();
            } else {
                alert('Error cancelling subscription: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            hideLoadingOverlay();
            alert('Error cancelling subscription');
            console.error('Error:', error);
        });
    }
}

function updatePayment() {
    showLoadingOverlay();
    fetch('/api/update-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingOverlay();
        if (data.url) {
            window.location.href = data.url;
        } else {
            alert('Error updating payment method');
        }
    })
    .catch(error => {
        hideLoadingOverlay();
        alert('Error updating payment method');
        console.error('Error:', error);
    });
}
