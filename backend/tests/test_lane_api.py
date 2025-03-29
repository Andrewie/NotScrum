import json
import pytest

def test_get_lanes(client, init_database):
    response = client.get('/api/lanes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['name'] == 'Todo'
    assert data[1]['name'] == 'Doing'
    assert data[2]['name'] == 'Done'

def test_get_board_lanes(client, init_database):
    response = client.get('/api/boards/1/lanes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['name'] == 'Todo'
    assert data[1]['name'] == 'Doing'
    assert data[2]['name'] == 'Done'

def test_get_lane(client, init_database):
    response = client.get('/api/lanes/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Todo'
    assert data['position'] == 0
    assert data['board_id'] == 1
    assert len(data['cards']) == 2  # Based on our test data

def test_create_lane(client, init_database):
    response = client.post(
        '/api/boards/1/lanes',
        data=json.dumps({'name': 'New Lane'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Lane'
    assert data['position'] == 3  # Should be added at the end
    assert data['board_id'] == 1

def test_update_lane(client, init_database):
    response = client.put(
        '/api/lanes/1',
        data=json.dumps({'name': 'Updated Lane', 'position': 3}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Lane'
    assert data['position'] == 3

def test_delete_lane(client, init_database):
    # First confirm lane exists
    response = client.get('/api/lanes/1')
    assert response.status_code == 200
    
    # Delete the lane
    response = client.delete('/api/lanes/1')
    assert response.status_code == 204
    
    # Confirm lane is deleted
    response = client.get('/api/lanes/1')
    assert response.status_code == 404

def test_reorder_lanes(client, init_database):
    # Current order: [1, 2, 3]
    # New order: [3, 1, 2]
    response = client.put(
        '/api/boards/1/lanes/reorder',
        data=json.dumps({'lane_order': [3, 1, 2]}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['id'] == 3
    assert data[1]['id'] == 1
    assert data[2]['id'] == 2