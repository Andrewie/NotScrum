# Simple Project Board

A simple, docker-based Kanban board application with drag-and-drop functionality, resembling post-it notes on a board.

## Features

- Drag and drop cards between lanes
- Create, edit, and delete cards and lanes
- Color-coded cards
- Optional due dates for cards
- Simple and intuitive interface
- Mobile-responsive design

## Technology Stack

- **Backend**: Python with Flask, SQLite database
- **Frontend**: React with TypeScript, TailwindCSS
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

2. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

3. Access the application in your browser:
   ```
   http://localhost:3000
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

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
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

## Data Export

To export your board data:

1. Navigate to a board
2. Click on the "Export" button
3. Choose between JSON or CSV format

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses [React Beautiful DnD](https://github.com/atlassian/react-beautiful-dnd) for drag-and-drop functionality
- Built with [Flask](https://flask.palletsprojects.com/) and [React](https://reactjs.org/)