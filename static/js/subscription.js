document.addEventListener('DOMContentLoaded', function() {
    const loadingOverlay = document.getElementById('loading-overlay');
    const successAlert = document.getElementById('success-alert');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');

    function showLoading() {
        loadingOverlay.classList.remove('d-none');
    }

    function hideLoading() {
        loadingOverlay.classList.add('d-none');
    }

    function showSuccess() {
        hideLoading();
        successAlert.classList.remove('d-none');
        setTimeout(() => {
            successAlert.classList.add('d-none');
        }, 5000);
    }

    function showError(message) {
        hideLoading();
        errorMessage.textContent = message;
        errorAlert.classList.remove('d-none');
        setTimeout(() => {
            errorAlert.classList.add('d-none');
        }, 7000);
    }

    paypal.Buttons({
        style: {
            shape: 'pill',
            color: 'gold',
            layout: 'vertical',
            label: 'subscribe'
        },
        createSubscription: function(data, actions) {
            showLoading();
            return actions.subscription.create({
                plan_id: 'P-9U345022LR302184VM67SLCA'
            }).catch(error => {
                console.error('Subscription creation error:', error);
                showError('Unable to create subscription. Please try again later.');
                return null;
            });
        },
        onApprove: function(data, actions) {
            console.log('Subscription ID:', data.subscriptionID);
            showSuccess();
            // Here you can add API call to your backend to save the subscription
        },
        onError: function(err) {
            console.error('PayPal error:', err);
            showError('An error occurred while processing your payment. Please try again later.');
        },
        onCancel: function() {
            hideLoading();
        }
    }).render('#paypal-button-container-P-9U345022LR302184VM67SLCA');
});