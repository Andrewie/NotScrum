from flask import Blueprint, jsonify, request
from .. import db
from ..models.card import Card

bp = Blueprint('cards', __name__, url_prefix='/api')

@bp.route('/cards', methods=['GET'])
def get_all_cards():
    """Get all cards"""
    cards = Card.query.all()
    return jsonify([card.to_dict() for card in cards]), 200

@bp.route('/cards', methods=['POST'])
def create_card():
    """Create a new card"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'lane_id' not in data:
        return jsonify({'error': 'Title and lane_id are required'}), 400
    
    # Find the highest position in the lane
    max_position = db.session.query(db.func.max(Card.position)).filter_by(
        lane_id=data.get('lane_id')).scalar() or 0
    
    card = Card(
        title=data.get('title'),
        description=data.get('description', ''),
        lane_id=data.get('lane_id'),
        position=max_position + 1,
        color=data.get('color', 'white')
    )
    
    db.session.add(card)
    db.session.commit()
    
    return jsonify(card.to_dict()), 201

@bp.route('/lanes/<int:lane_id>/cards', methods=['GET'])
def get_cards_by_lane(lane_id):
    """Get all cards for a specific lane"""
    cards = Card.query.filter_by(lane_id=lane_id).order_by(Card.position).all()
    return jsonify([card.to_dict() for card in cards]), 200

@bp.route('/lanes/<int:lane_id>/cards', methods=['POST'])
def create_card_in_lane(lane_id):
    """Create a new card in a specific lane"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Find the highest position in the lane
    max_position = db.session.query(db.func.max(Card.position)).filter_by(
        lane_id=lane_id).scalar() or 0
    
    card = Card(
        title=data.get('title'),
        description=data.get('description', ''),
        lane_id=lane_id,
        position=max_position + 1,
        color=data.get('color', 'white')
    )
    
    db.session.add(card)
    db.session.commit()
    
    return jsonify(card.to_dict()), 201

@bp.route('/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    """Get a card by ID"""
    card = Card.query.get_or_404(card_id)
    return jsonify(card.to_dict()), 200

@bp.route('/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    """Update a card"""
    card = Card.query.get_or_404(card_id)
    data = request.get_json()
    
    if data.get('title'):
        card.title = data.get('title')
    if data.get('description') is not None:
        card.description = data.get('description')
    if data.get('lane_id') is not None:
        card.lane_id = data.get('lane_id')
    if data.get('position') is not None:
        card.position = data.get('position')
    if data.get('color'):
        card.color = data.get('color')
    if data.get('due_date') is not None:
        card.due_date = data.get('due_date')
    
    db.session.commit()
    
    return jsonify(card.to_dict()), 200

@bp.route('/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Delete a card"""
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    
    return jsonify({'message': 'Card deleted successfully'}), 200
