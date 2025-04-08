from flask import jsonify, request
from app import db
from app.api import bp
from app.models.card import Card
from app.models.lane import Lane
from datetime import datetime

@bp.route('/cards', methods=['GET'])
def get_cards():
    cards = Card.query.all()
    return jsonify([card.to_dict() for card in cards])

@bp.route('/lanes/<int:lane_id>/cards', methods=['GET'])
def get_lane_cards(lane_id):
    lane = Lane.query.get_or_404(lane_id)
    cards = Card.query.filter_by(lane_id=lane_id).order_by(Card.position).all()
    return jsonify([card.to_dict() for card in cards])

@bp.route('/cards/<int:id>', methods=['GET'])
def get_card(id):
    card = Card.query.get_or_404(id)
    return jsonify(card.to_dict())

@bp.route('/lanes/<int:lane_id>/cards', methods=['POST'])
def create_card(lane_id):
    lane = Lane.query.get_or_404(lane_id)
    data = request.get_json() or {}
    
    if 'title' not in data:
        return jsonify({'error': 'Missing required field: title'}), 400
    
    # If position is not specified, add to the end
    if 'position' not in data:
        max_position = db.session.query(db.func.max(Card.position)).filter_by(lane_id=lane_id).scalar() or -1
        position = max_position + 1
    else:
        position = data['position']
    
    # Handle due_date if provided
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format for due_date. Use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)'}), 400
    
    card = Card(
        title=data['title'],
        description=data.get('description', ''),
        color=data.get('color', 'white'),
        position=position,
        due_date=due_date,
        lane_id=lane_id
    )
    
    db.session.add(card)
    db.session.commit()
    return jsonify(card.to_dict()), 201

@bp.route('/cards/<int:id>', methods=['PUT'])
def update_card(id):
    card = Card.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'title' in data:
        card.title = data['title']
    if 'description' in data:
        card.description = data['description']
    if 'color' in data:
        card.color = data['color']
    if 'position' in data:
        card.position = data['position']
    if 'due_date' in data:
        # Handle due_date if provided
        if data['due_date']:
            try:
                card.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid date format for due_date. Use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)'}), 400
        else:
            card.due_date = None
    if 'lane_id' in data:
        # Verify lane exists before moving card
        lane = Lane.query.get_or_404(data['lane_id'])
        card.lane_id = data['lane_id']
    
    db.session.commit()
    return jsonify(card.to_dict())

@bp.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return '', 204

@bp.route('/lanes/<int:lane_id>/cards/reorder', methods=['PUT'])
def reorder_cards(lane_id):
    lane = Lane.query.get_or_404(lane_id)
    data = request.get_json() or {}
    
    if 'card_order' not in data:
        return jsonify({'error': 'Missing required field: card_order'}), 400
    
    card_order = data['card_order']
    
    # Update positions
    for index, card_id in enumerate(card_order):
        card = Card.query.get_or_404(card_id)
        if card.lane_id != lane_id:
            return jsonify({'error': f'Card {card_id} does not belong to lane {lane_id}'}), 400
        card.position = index
    
    db.session.commit()
    cards = Card.query.filter_by(lane_id=lane_id).order_by(Card.position).all()
    return jsonify([card.to_dict() for card in cards])

@bp.route('/cards/<int:id>/move', methods=['PUT'])
def move_card(id):
    card = Card.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'lane_id' not in data:
        return jsonify({'error': 'Missing required field: lane_id'}), 400
    
    target_lane_id = data['lane_id']
    target_position = data.get('position')
    
    # Verify the target lane exists
    target_lane = Lane.query.get_or_404(target_lane_id)
    
    # If position is not specified, add to the end
    if target_position is None:
        max_position = db.session.query(db.func.max(Card.position)).filter_by(lane_id=target_lane_id).scalar() or -1
        target_position = max_position + 1
    
    card.lane_id = target_lane_id
    card.position = target_position
    
    # Reorder cards in the target lane
    if 'card_order' in data:
        card_order = data['card_order']
        for index, card_id in enumerate(card_order):
            c = Card.query.get_or_404(card_id)
            if c.lane_id != target_lane_id:
                return jsonify({'error': f'Card {card_id} does not belong to lane {target_lane_id}'}), 400
            c.position = index
    
    db.session.commit()
    return jsonify(card.to_dict())
