import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /api/health endpoint."""
    rv = client.get('/api/health')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'healthy'

def test_metrics_endpoint(client):
    """Test the /metrics endpoint."""
    rv = client.get('/metrics')
    assert rv.status_code == 200
    assert b'http_requests_total' in rv.data

def test_scheduler_jobs(client):
    """Test the /api/scheduler/jobs endpoint."""
    rv = client.get('/api/scheduler/jobs')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'running'
    # Should have at least 3 jobs (Morning, Evening, Archive, Backup)
    assert len(json_data['jobs']) >= 3
