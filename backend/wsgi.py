from app import create_app, db
from app.models.board import Board
from app.models.lane import Lane
from app.models.card import Card

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Board': Board,
        'Lane': Lane,
        'Card': Card
    }