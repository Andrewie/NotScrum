import os
import sys
import pytest
from app import create_app, db
from app.models.board import Board
from app.models.lane import Lane
from app.models.card import Card

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Create a test board
        board = Board(name='Test Board', description='Test Description')
        db.session.add(board)
        db.session.commit()
        
        # Create test lanes
        lanes = [
            Lane(name='Todo', position=0, board_id=board.id),
            Lane(name='Doing', position=1, board_id=board.id),
            Lane(name='Done', position=2, board_id=board.id)
        ]
        db.session.add_all(lanes)
        db.session.commit()
        
        # Create test cards
        cards = [
            Card(title='Card 1', description='Description 1', position=0, lane_id=lanes[0].id),
            Card(title='Card 2', description='Description 2', position=1, lane_id=lanes[0].id),
            Card(title='Card 3', description='Description 3', position=0, lane_id=lanes[1].id)
        ]
        db.session.add_all(cards)
        db.session.commit()
        
        yield