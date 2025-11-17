import json
import pytest
import pandas as pd
from unittest.mock import patch

# Import the app. This will be the real or fake Flask app.
from backend.api.app import app

# Determine if we are in fallback mode
IS_FALLBACK = not hasattr(app, 'test_client')

@pytest.fixture
def client():
    """Create a test client for the app, supporting both Flask and the fallback."""
    if IS_FALLBACK:
        # The fallback app has a built-in fake client
        return app.test_client()
    else:
        # Use the standard Flask test client
        with app.test_client() as client:
            yield client

@patch('backend.api.app.fetch_latest')
@patch('backend.api.app.predict_signal')
def test_predict_endpoint_success(mock_predict_signal, mock_fetch_latest, client):
    """
    Tests the /predict/<symbol> endpoint for a successful response.
    Mocks fetcher and predictor to isolate API logic.
    """
    # Arrange: Configure mocks
    symbol = "TESTSYMBOL"
    mock_fetch_latest.return_value = pd.DataFrame({'Close': [100, 110, 120]})
    mock_predict_signal.return_value = {
        "signal": "BUY",
        "confidence": 0.88,
        "reason": "MA9 crossed above MA21 and RSI is strong."
    }

    # Act: Make the request
    response = client.get(f'/predict/{symbol}')

    # Assert: Check the response
    assert response.status_code == 200

    # The response object and data format differ between Flask and the fallback
    if IS_FALLBACK:
        response_data = response.get_json()
    else:
        response_data = json.loads(response.data)

    assert response_data['symbol'] == symbol
    assert response_data['signal'] == "BUY"
    assert response_data['confidence'] == 0.88
    assert 'reason' in response_data

    # Verify that our mocks were called
    mock_fetch_latest.assert_called_once_with(symbol)
    mock_predict_signal.assert_called_once()

def test_predict_endpoint_no_symbol(client):
    """
    Tests the API's response when no symbol is provided.
    Note: This route is not matched by the simple fallback client, so it only runs for Flask.
    """
    if not IS_FALLBACK:
        response = client.get('/predict/')
        assert response.status_code == 404 # Flask returns 404 for unmatched routes
