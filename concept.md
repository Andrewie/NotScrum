# Simple Project Board

## Overview
This document outlines the concept of a web application, Simple Project Board. A simple Todo, doing, done board system with cards resembling post-it notes.

## UX Features
- **Drag and drop cards into lanes**
- **One tap to create new card**
- **Double tap to edit a card**
- **Color-coding for different card types or priorities**
- **Simple filtering and search functionality**
- **Optional deadline/date tracking for cards**
- **Mobile-responsive design**
- **Minimal onboarding required - intuitive interface**

## Core Functionality
- **Boards**: Create multiple boards for different projects
- **Lanes**: Customizable lanes (default: Todo, Doing, Done)
- **Cards**: Create, edit, delete, and move cards between lanes
- **Persistence**: All changes saved automatically
- **Data Export**: Simple JSON/CSV export option

## Technology Stack
### Backend
- **Python and Flask** for the backend
- **RESTful API** ready for multiple frontend apps
- **SQLite** database for simplicity and ease of deployment
- **Flask-SQLAlchemy** for ORM
- **Flask-Migrate** for database migrations
- **Flask-CORS** for cross-origin requests

### Frontend
- **React** with **TypeScript** for type safety
- **React Beautiful DnD** for drag and drop functionality
- **Styled Components** or **TailwindCSS** for styling
- **Axios** for API communication

### Deployment
- **Docker** and **Docker Compose** for containerization
- **Nginx** as reverse proxy (optional)
- **Single docker-compose.yml** file for easy setup

## Minimum Viable Product (MVP)
1. Single board with three lanes (Todo, Doing, Done)
2. Create, edit, and delete cards
3. Move cards between lanes
4. Persistent storage of all data
5. Basic styling resembling post-it notes

## Future Enhancements
- User authentication
- Multiple boards
- Card comments and attachments
- Activity history/logs
- Team collaboration features
- Custom labels or tags

## Development Approach
1. Set up basic Flask API with SQLite
2. Create React frontend with basic UI
3. Implement drag and drop functionality
4. Connect frontend to backend API
5. Containerize with Docker
6. Add additional features based on priority

## Simplicity Focus
- Single command to start the entire application
- No complex configuration required
- Self-contained application with embedded database
- Clear documentation for setup and usage
- Optimized for developer experience
