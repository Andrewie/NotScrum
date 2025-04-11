# Simple Project Board (Backend)

A simple, docker-based Kanban board application with a RESTful API backend. This repository contains only the backend service, the frontend is now hosted separately.

## Features

- RESTful API for managing boards, lanes, and cards
- SQLite database for data persistence
- Docker containerization for easy deployment
- Complete API for Kanban board operations

## Technology Stack

- **Backend**: Python with Flask, SQLite database
- **Deployment**: Docker and Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd notscrum
   ```

2. Start the backend service using Docker Compose:
   ```
   docker-compose up -d
   ```

3. The backend API will be available at:
   ```
   http://localhost:5000/api
   ```

### Development Setup

If you want to set up the development environment without Docker:

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Run the development server:
   ```
   flask run
   ```

## API Documentation

The backend provides a RESTful API for managing boards, lanes, and cards.

### Boards

- `GET /api/boards` - Get all boards
- `GET /api/boards/<id>` - Get a specific board
- `POST /api/boards` - Create a new board
- `PUT /api/boards/<id>` - Update a board
- `DELETE /api/boards/<id>` - Delete a board

### Lanes

- `GET /api/lanes` - Get all lanes
- `GET /api/boards/<board_id>/lanes` - Get lanes for a specific board
- `GET /api/lanes/<id>` - Get a specific lane
- `POST /api/boards/<board_id>/lanes` - Create a new lane
- `PUT /api/lanes/<id>` - Update a lane
- `DELETE /api/lanes/<id>` - Delete a lane
- `PUT /api/boards/<board_id>/lanes/reorder` - Reorder lanes in a board

### Cards

- `GET /api/cards` - Get all cards
- `GET /api/lanes/<lane_id>/cards` - Get cards for a specific lane
- `GET /api/cards/<id>` - Get a specific card
- `POST /api/lanes/<lane_id>/cards` - Create a new card
- `PUT /api/cards/<id>` - Update a card
- `DELETE /api/cards/<id>` - Delete a card
- `PUT /api/lanes/<lane_id>/cards/reorder` - Reorder cards in a lane
- `PUT /api/cards/<id>/move` - Move a card to a different lane

## License

[MIT License](LICENSE)

## Acknowledgements

- Built with [Flask](https://flask.palletsprojects.com/)