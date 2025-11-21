document.addEventListener('DOMContentLoaded', () => {
    const predictBtn = document.getElementById('predict-btn');
    const symbolInput = document.getElementById('symbol-input');
    const signalValue = document.getElementById('signal-value');
    const confidenceValue = document.getElementById('confidence-value');
    const reasonValue = document.getElementById('reason-value');
    const errorMessage = document.getElementById('error-message');

    predictBtn.addEventListener('click', async () => {
        const symbol = symbolInput.value.trim().toUpperCase();

        // Reset UI
        errorMessage.textContent = '';
        signalValue.textContent = '-';
        confidenceValue.textContent = '-';
        reasonValue.textContent = '-';

        if (!symbol) {
            errorMessage.textContent = 'Error: Symbol cannot be empty.';
            return;
        }

        try {
            // In a real environment, the port might differ or be omitted (if using a proxy)
            const response = await fetch(`https://gitta-trader-ai.onrender.com/api/analysis/stock/prediction/${symbol}`);

            if (!response.ok) {
                throw new Error(`Server error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();

            if (!data.signal || !data.confidence || !data.reason) {
                 throw new Error('Invalid response format from server.');
            }

            signalValue.textContent = data.signal;
            confidenceValue.textContent = data.confidence.toFixed(2);
            reasonValue.textContent = data.reason;

        } catch (error) {
            console.error('Fetch error:', error);
            errorMessage.textContent = `Error: Could not fetch prediction. ${error.message}. Is the backend server running?`;
            // Simulate data for frontend development if backend is down
            if (error instanceof TypeError) { // This often indicates a network error
                errorMessage.textContent += ' Displaying simulated data.';
                signalValue.textContent = 'BUY';
                confidenceValue.textContent = '0.88';
                reasonValue.textContent = 'Simulated response for frontend testing.';
            }
        }
    });
});
