from jynx_ui.application import app
from jynx_ui.routes import bot_response
from unittest.mock import MagicMock, patch
import pytest
import json


#############################################################################
#routes.py Testing
#############################################################################

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'<title>Jynx AI</title>' in response.data

def test_favicon(client):
    response = client.get('/favicon.ico')
    assert response.status_code == 200
    assert response.mimetype == 'image/vnd.microsoft.icon'

def test_submit_message(client):
    response = client.post('/submit_message', json={'message': 'Test message', 'chat_name': 'test_chat'})
    assert response.status_code == 200
    assert b'status' in response.data
    assert b'message' in response.data

def test_chat_list(client):
    response = client.get('/chat_list')
    assert response.status_code == 200
    assert b'chat_count' in response.data
    assert b'chatList' in response.data

def test_chat_load(client):
    response = client.post('/chat_load', json={'chatName': 'test_chat'})
    assert response.status_code == 200
    assert b'chats' in response.data

def test_chat_create(client):
    response = client.get('/chat_create')
    assert response.status_code == 200
    assert b'status' in response.data
    assert b'chat_count' in response.data
    assert b'chat_name' in response.data

def test_bot_response():
    # Mocking the requests.post method to simulate a response
    with patch('requests.post') as mock_post:
        # Mocking the response object
        mock_response = MagicMock()
        mock_response.text = '{"status": true, "message": "warning - no task run."}'
        mock_post.return_value = mock_response

        # Testing bot_response function
        response = bot_response("refresh ae16")
        assert response["status"] == True
        assert response["message"] == "warning - no task run."

def test_submit_message_error(client):
    # Simulating an error response from the bot
    with patch('requests.post') as mock_post:
        # Mocking the response object
        mock_response = MagicMock()
        mock_response.text = '{"error": "Internal server error"}'
        mock_post.return_value = mock_response

        # Testing submit_message function with error response
        response = client.post('/submit_message', json={'message': 'ae16 deployment', 'chat_name': 'test_chat'})
        assert response.status_code == 200
        assert b'status' in response.data
        assert b'message' in response.data

def test_submit_integration_test(client):
    # Testing submit_message function with actual POST data
    response = client.post('/submit_message', json={'message': 'ae16 deployment', 'chat_name': 'test_chat'})
    
    # Asserting the response
    assert response.status_code == 200
    assert b'status' in response.data
    assert b'message' in response.data

    response_data = json.loads(response.data)
    assert response_data["status"] == True

#############################################################################
#__main__.py Testing
#############################################################################

def test_main():
    with patch.object(app, 'run') as mock_run:
        import __main__
        assert mock_run.called_once_with(host=app.config['HOST'], port=app.config['PORT'])
