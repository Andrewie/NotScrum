import json
import pytest

def test_get_boards(client, init_database):
    response = client.get('/api/boards')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Board'
    assert data[0]['description'] == 'Test Description'

def test_get_board(client, init_database):
    response = client.get('/api/boards/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Board'
    assert data['description'] == 'Test Description'
    assert len(data['lanes']) == 3

def test_create_board(client):
    response = client.post(
        '/api/boards',
        data=json.dumps({'name': 'New Board', 'description': 'New Description'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Board'
    assert data['description'] == 'New Description'
    # Should create default lanes
    assert len(data['lanes']) == 3
    assert data['lanes'][0]['name'] == 'Todo'
    assert data['lanes'][1]['name'] == 'Doing'
    assert data['lanes'][2]['name'] == 'Done'

def test_update_board(client, init_database):
    response = client.put(
        '/api/boards/1',
        data=json.dumps({'name': 'Updated Board', 'description': 'Updated Description'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Board'
    assert data['description'] == 'Updated Description'

def test_delete_board(client, init_database):
    # First confirm board exists
    response = client.get('/api/boards/1')
    assert response.status_code == 200
    
    # Delete the board
    response = client.delete('/api/boards/1')
    assert response.status_code == 204
    
    # Confirm board is deleted
    response = client.get('/api/boards/1')
    assert response.status_code == 404