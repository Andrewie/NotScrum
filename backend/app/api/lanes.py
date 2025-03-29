from flask import jsonify, request
from app import db
from app.api import bp
from app.models.lane import Lane
from app.models.board import Board

@bp.route('/lanes', methods=['GET'])
def get_lanes():
    lanes = Lane.query.all()
    return jsonify([lane.to_dict() for lane in lanes])

@bp.route('/boards/<int:board_id>/lanes', methods=['GET'])
def get_board_lanes(board_id):
    board = Board.query.get_or_404(board_id)
    lanes = Lane.query.filter_by(board_id=board_id).order_by(Lane.position).all()
    return jsonify([lane.to_dict() for lane in lanes])

@bp.route('/lanes/<int:id>', methods=['GET'])
def get_lane(id):
    lane = Lane.query.get_or_404(id)
    return jsonify(lane.to_dict())

@bp.route('/boards/<int:board_id>/lanes', methods=['POST'])
def create_lane(board_id):
    board = Board.query.get_or_404(board_id)
    data = request.get_json() or {}
    
    if 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    # If position is not specified, add to the end
    if 'position' not in data:
        max_position = db.session.query(db.func.max(Lane.position)).filter_by(board_id=board_id).scalar() or -1
        position = max_position + 1
    else:
        position = data['position']
    
    lane = Lane(
        name=data['name'],
        position=position,
        board_id=board_id
    )
    
    db.session.add(lane)
    db.session.commit()
    return jsonify(lane.to_dict()), 201

@bp.route('/lanes/<int:id>', methods=['PUT'])
def update_lane(id):
    lane = Lane.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'name' in data:
        lane.name = data['name']
    if 'position' in data:
        lane.position = data['position']
    
    db.session.commit()
    return jsonify(lane.to_dict())

@bp.route('/lanes/<int:id>', methods=['DELETE'])
def delete_lane(id):
    lane = Lane.query.get_or_404(id)
    db.session.delete(lane)
    db.session.commit()
    return '', 204

@bp.route('/boards/<int:board_id>/lanes/reorder', methods=['PUT'])
def reorder_lanes(board_id):
    board = Board.query.get_or_404(board_id)
    data = request.get_json() or {}
    
    if 'lane_order' not in data:
        return jsonify({'error': 'Missing required field: lane_order'}), 400
    
    lane_order = data['lane_order']
    
    # Update positions
    for index, lane_id in enumerate(lane_order):
        lane = Lane.query.get_or_404(lane_id)
        if lane.board_id != board_id:
            return jsonify({'error': f'Lane {lane_id} does not belong to board {board_id}'}), 400
        lane.position = index
    
    db.session.commit()
    lanes = Lane.query.filter_by(board_id=board_id).order_by(Lane.position).all()
    return jsonify([lane.to_dict() for lane in lanes])