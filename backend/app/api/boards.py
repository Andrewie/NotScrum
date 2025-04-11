from flask import Blueprint, jsonify, request
from .. import db
from ..models.board import Board
from ..models.lane import Lane

bp = Blueprint('boards', __name__, url_prefix='/api')

@bp.route('/boards', methods=['GET'])
def get_all_boards():
    """Get all boards"""
    boards = Board.query.all()
    return jsonify([{
        'id': board.id,
        'name': board.name,
        'description': board.description
    } for board in boards]), 200

@bp.route('/boards', methods=['POST'])
def create_board():
    """Create a new board"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    board = Board(
        name=data.get('name'),
        description=data.get('description', '')
    )
    db.session.add(board)
    db.session.commit()
    
    # Create default lanes
    default_lanes = ['To Do', 'In Progress', 'Done']
    position = 1
    
    for lane_title in default_lanes:
        lane = Lane(name=lane_title, board_id=board.id, position=position)
        db.session.add(lane)
        position += 1
    
    db.session.commit()
    
    return jsonify({
        'id': board.id,
        'name': board.name,
        'description': board.description
    }), 201

@bp.route('/boards/<int:board_id>', methods=['GET'])
def get_board(board_id):
    """Get a board by ID with its lanes"""
    board = Board.query.get_or_404(board_id)
    # Get lanes ordered by position
    lanes = Lane.query.filter_by(board_id=board_id).order_by(Lane.position).all()
    
    # Format the response with board data and lanes
    board_data = {
        'id': board.id,
        'name': board.name,
        'description': board.description,
        'lanes': [{
            'id': lane.id,
            'name': lane.name,
            'board_id': lane.board_id,
            'position': lane.position,
            'cards': [] # Cards will be loaded separately
        } for lane in lanes]
    }
    
    return jsonify(board_data), 200

@bp.route('/boards/<int:board_id>', methods=['PUT'])
def update_board(board_id):
    """Update a board"""
    board = Board.query.get_or_404(board_id)
    data = request.get_json()
    
    if data.get('name'):
        board.name = data.get('name')
    if data.get('description') is not None:
        board.description = data.get('description')
    
    db.session.commit()
    
    return jsonify({
        'id': board.id,
        'name': board.name,
        'description': board.description
    }), 200

@bp.route('/boards/<int:board_id>', methods=['DELETE'])
def delete_board(board_id):
    """Delete a board"""
    board = Board.query.get_or_404(board_id)
    db.session.delete(board)
    db.session.commit()
    
    return jsonify({'message': 'Board deleted successfully'}), 200

@bp.route('/boards/<int:board_id>/lanes', methods=['GET'])
def get_board_lanes(board_id):
    """Get all lanes for a board"""
    Board.query.get_or_404(board_id)  # Check if board exists
    lanes = Lane.query.filter_by(board_id=board_id).order_by(Lane.position).all()
    
    return jsonify([{
        'id': lane.id,
        'name': lane.name,
        'board_id': lane.board_id,
        'position': lane.position
    } for lane in lanes]), 200

@bp.route('/boards/<int:board_id>/lanes', methods=['POST'])
def create_board_lane(board_id):
    """Create a new lane for a specific board"""
    board = Board.query.get_or_404(board_id)  # Check if board exists
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Find the highest position in the board
    max_position = db.session.query(db.func.max(Lane.position)).filter_by(
        board_id=board_id).scalar() or 0
    
    # Use provided position or calculate based on existing lanes
    position = data.get('position') if data.get('position') is not None else max_position + 1
    
    lane = Lane(
        name=data.get('name'),
        board_id=board_id,
        position=position
    )
    
    db.session.add(lane)
    db.session.commit()
    
    return jsonify({
        'id': lane.id,
        'name': lane.name,
        'board_id': lane.board_id,
        'position': lane.position
    }), 201
