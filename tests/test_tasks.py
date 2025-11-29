import pytest
from app import create_app
from src.models.user import db

@pytest.fixture
def client():
    """Setup test client with in-memory database"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_task(client):
    """Test creating a new task"""
    # First need to register and login
    response = client.post('/api/users/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    token = response.json['access_token']

    # Create a task
    response = client.post('/api/tasks',
        json={
            'title': 'Test Task',
            'description': 'Test description',
            'priority': 'high'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.json['title'] == 'Test Task'
    assert response.json['priority'] == 'high'

def test_get_tasks(client):
    """Test getting all tasks"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_task_by_id(client):
    """Test getting a specific task"""
    # TODO: Create a task first, then retrieve it
    # TODO: Test error case when task doesn't exist
    pass

# TODO: Add test for updating tasks
# TODO: Add test for deleting tasks
# TODO: Add test for filtering by status
# TODO: Add test for filtering by priority
# TODO: Add test for authentication requirements on protected endpoints
# NOTE: Should we test pagination once it's implemented?
# FIXME: Missing tests for error cases (invalid priority, missing required fields, etc.)