from flask import jsonify, request
from app import db
from app.api import bp
from app.models.board import Board
from app.models.lane import Lane

@bp.route('/boards', methods=['GET'])
def get_boards():
    boards = Board.query.all()
    return jsonify([board.to_dict() for board in boards])

@bp.route('/boards/<int:id>', methods=['GET'])
def get_board(id):
    board = Board.query.get_or_404(id)
    return jsonify(board.to_dict())

@bp.route('/boards', methods=['POST'])
def create_board():
    data = request.get_json() or {}
    if 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    board = Board(name=data['name'], description=data.get('description', ''))
    
    # If no lanes are specified, create default Todo, Doing, Done lanes
    if 'lanes' not in data or not data['lanes']:
        default_lanes = [
            {'name': 'Todo', 'position': 0},
            {'name': 'Doing', 'position': 1},
            {'name': 'Done', 'position': 2}
        ]
        for lane_data in default_lanes:
            lane = Lane(name=lane_data['name'], position=lane_data['position'])
            board.lanes.append(lane)
    
    db.session.add(board)
    db.session.commit()
    return jsonify(board.to_dict()), 201

@bp.route('/boards/<int:id>', methods=['PUT'])
def update_board(id):
    board = Board.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'name' in data:
        board.name = data['name']
    if 'description' in data:
        board.description = data['description']
    
    db.session.commit()
    return jsonify(board.to_dict())

@bp.route('/boards/<int:id>', methods=['DELETE'])
def delete_board(id):
    board = Board.query.get_or_404(id)
    db.session.delete(board)
    db.session.commit()
    return '', 204
