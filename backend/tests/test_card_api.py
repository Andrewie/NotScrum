import json
import pytest

def test_get_cards(client, init_database):
    response = client.get('/api/cards')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['title'] == 'Card 1'
    assert data[1]['title'] == 'Card 2'
    assert data[2]['title'] == 'Card 3'

def test_get_lane_cards(client, init_database):
    response = client.get('/api/lanes/1/cards')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] == 'Card 1'
    assert data[1]['title'] == 'Card 2'

def test_get_card(client, init_database):
    response = client.get('/api/cards/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Card 1'
    assert data['description'] == 'Description 1'
    assert data['position'] == 0
    assert data['lane_id'] == 1

def test_create_card(client, init_database):
    response = client.post(
        '/api/lanes/1/cards',
        data=json.dumps({
            'title': 'New Card',
            'description': 'New Description',
            'color': 'blue'
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Card'
    assert data['description'] == 'New Description'
    assert data['color'] == 'blue'
    assert data['position'] == 2  # Should be added at the end
    assert data['lane_id'] == 1

def test_update_card(client, init_database):
    response = client.put(
        '/api/cards/1',
        data=json.dumps({
            'title': 'Updated Card',
            'description': 'Updated Description',
            'color': 'green'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Card'
    assert data['description'] == 'Updated Description'
    assert data['color'] == 'green'

def test_delete_card(client, init_database):
    # First confirm card exists
    response = client.get('/api/cards/1')
    assert response.status_code == 200
    
    # Delete the card
    response = client.delete('/api/cards/1')
    assert response.status_code == 204
    
    # Confirm card is deleted
    response = client.get('/api/cards/1')
    assert response.status_code == 404

def test_move_card(client, init_database):
    # Move card from lane 1 to lane 2
    response = client.put(
        '/api/cards/1/move',
        data=json.dumps({
            'lane_id': 2,
            'position': 1
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['lane_id'] == 2
    assert data['position'] == 1
    
    # Check card is in the new lane
    response = client.get('/api/lanes/2/cards')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[1]['id'] == 1

def test_reorder_cards(client, init_database):
    # Lane 1 has cards 1 and 2
    # Current order: [1, 2]
    # New order: [2, 1]
    response = client.put(
        '/api/lanes/1/cards/reorder',
        data=json.dumps({'card_order': [2, 1]}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['id'] == 2
    assert data[1]['id'] == 1