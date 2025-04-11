from flask import Blueprint, jsonify, request
from .. import db
from ..models.lane import Lane
from ..models.card import Card

bp = Blueprint('lanes', __name__, url_prefix='/api')

@bp.route('/lanes', methods=['GET'])
def get_all_lanes():
    """Get all lanes"""
    lanes = Lane.query.all()
    return jsonify([{
        'id': lane.id,
        'name': lane.name,
        'board_id': lane.board_id,
        'position': lane.position
    } for lane in lanes]), 200

@bp.route('/lanes', methods=['POST'])
def create_lane():
    """Create a new lane"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'board_id' not in data:
        return jsonify({'error': 'Name and board_id are required'}), 400
    
    # Find the highest position in the board
    max_position = db.session.query(db.func.max(Lane.position)).filter_by(
        board_id=data.get('board_id')).scalar() or 0
    
    lane = Lane(
        name=data.get('name'),
        board_id=data.get('board_id'),
        position=max_position + 1
    )
    
    db.session.add(lane)
    db.session.commit()
    
    return jsonify({
        'id': lane.id,
        'name': lane.name,
        'board_id': lane.board_id,
        'position': lane.position
    }), 201

@bp.route('/lanes/<int:lane_id>', methods=['GET'])
def get_lane(lane_id):
    """Get a lane by ID"""
    lane = Lane.query.get_or_404(lane_id)
    return jsonify({
        'id': lane.id,
        'name': lane.name,
        'board_id': lane.board_id,
        'position': lane.position
    }), 200

@bp.route('/lanes/<int:lane_id>', methods=['PUT'])
def update_lane(lane_id):
    """Update a lane"""
    lane = Lane.query.get_or_404(lane_id)
    data = request.get_json()
    
    if data.get('name'):
        lane.name = data.get('name')
    if data.get('position') is not None:
        lane.position = data.get('position')
    
    db.session.commit()
    
    return jsonify({
        'id': lane.id,
        'name': lane.name,
        'board_id': lane.board_id,
        'position': lane.position
    }), 200

@bp.route('/lanes/<int:lane_id>', methods=['DELETE'])
def delete_lane(lane_id):
    """Delete a lane"""
    lane = Lane.query.get_or_404(lane_id)
    db.session.delete(lane)
    db.session.commit()
    
    return jsonify({'message': 'Lane deleted successfully'}), 200

@bp.route('/lanes/<int:lane_id>/cards', methods=['GET'])
def get_lane_cards(lane_id):
    """Get all cards for a lane"""
    Lane.query.get_or_404(lane_id)  # Check if lane exists
    cards = Card.query.filter_by(lane_id=lane_id).order_by(Card.position).all()
    
    return jsonify([{
        'id': card.id,
        'title': card.title,
        'description': card.description,
        'lane_id': card.lane_id,
        'position': card.position,
        'color': card.color
    } for card in cards]), 200
