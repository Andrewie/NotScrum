#!/bin/sh
# Initialize the database on first run

# Wait for the Flask app to be ready
echo "Waiting for Flask application to start..."
sleep 10

# Check if the instance directory exists, if not create it
if [ ! -d "instance" ]; then
    echo "Creating instance directory..."
    mkdir -p instance
fi

# Check if any migrations exist
if [ ! -d "migrations" ]; then
    echo "Initializing database migrations..."
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    echo "Database initialized successfully!"
else
    echo "Applying existing migrations..."
    flask db upgrade
    echo "Migrations applied successfully!"
fi

# Create sample data if the database is empty
echo "Checking if sample data needs to be created..."
BOARD_COUNT=$(flask shell -c "from app.models.board import Board; print(Board.query.count())" 2>/dev/null || echo "0")

if [ "$BOARD_COUNT" = "0" ]; then
    echo "Creating sample data..."
    # Create a Python script for sample data
    cat > create_sample_data.py << EOF
from app.models.board import Board
from app.models.lane import Lane
from app.models.card import Card
from app import db

# Create a sample board
board = Board(name='Sample Board', description='This is a sample board created automatically')
db.session.add(board)
db.session.commit()

# Create sample lanes
lanes = [
    Lane(name='To Do', board_id=board.id, position=0),
    Lane(name='In Progress', board_id=board.id, position=1),
    Lane(name='Done', board_id=board.id, position=2)
]
db.session.add_all(lanes)
db.session.commit()

# Create sample cards
cards = [
    Card(title='Welcome to NotScrum', description='This is a sample card to get you started.', lane_id=lanes[0].id, position=0),
    Card(title='Try dragging this card', description='You can drag cards between lanes to update their status.', lane_id=lanes[0].id, position=1),
    Card(title='Create a new card', description='Click the + Add Card button at the bottom of a lane.', lane_id=lanes[1].id, position=0),
    Card(title='Sample completed task', description='This is a sample of a completed task.', lane_id=lanes[2].id, position=0)
]
db.session.add_all(cards)
db.session.commit()

print('Sample data created successfully!')
EOF
    # Run the script with flask shell
    flask shell < create_sample_data.py
    # Remove the temporary script
    rm create_sample_data.py
    echo "Sample data created successfully!"
fi

echo "Database initialization complete!"