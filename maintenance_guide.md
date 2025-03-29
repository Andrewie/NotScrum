# NotScrum Maintenance Guide

This document outlines the maintenance procedures for the NotScrum application, including database management, troubleshooting, updating, and backing up the system.

## Environment Management

### Configuration

The application uses environment variables for configuration. These are set in:
- Backend: `.env` file in the backend directory or environment variables in the Docker container
- Frontend: Environment variables passed to the Docker container

Key configuration variables:
- `FLASK_ENV`: Set to `development` or `production`
- `FLASK_DEBUG`: Set to `1` for debug mode, `0` for production
- `REACT_APP_API_URL`: The URL of the backend API

### Updating Environment Variables

1. To update environment variables in Docker:
   ```
   docker-compose down
   # Edit the docker-compose.yml file
   docker-compose up -d
   ```

2. To update environment variables in the backend `.env` file:
   ```
   # Edit the .env file
   # Restart the backend service
   docker-compose restart backend
   ```

## Database Management

The application uses SQLite for data storage, with the database file stored in a Docker volume.

### Database Migrations

When making changes to the database schema:

1. Create a new migration:
   ```
   docker-compose exec backend flask db migrate -m "Description of changes"
   ```

2. Apply the migration:
   ```
   docker-compose exec backend flask db upgrade
   ```

3. Rollback a migration if needed:
   ```
   docker-compose exec backend flask db downgrade
   ```

### Database Backup

1. Create a backup of the SQLite database:
   ```
   docker-compose exec backend sh -c "sqlite3 instance/app.db .dump > /app/backup_$(date +%Y%m%d_%H%M%S).sql"
   ```

2. Copy the backup file to the host:
   ```
   docker cp notscrum-backend:/app/backup_YYYYMMDD_HHMMSS.sql ./backups/
   ```

### Database Restore

1. Copy the backup file to the container:
   ```
   docker cp ./backups/backup_YYYYMMDD_HHMMSS.sql notscrum-backend:/app/
   ```

2. Restore the database:
   ```
   docker-compose exec backend sh -c "cat /app/backup_YYYYMMDD_HHMMSS.sql | sqlite3 instance/app.db"
   ```

## Application Updates

### Backend Updates

1. Pull the latest code:
   ```
   git pull origin main
   ```

2. Rebuild and restart the backend container:
   ```
   docker-compose build backend
   docker-compose up -d backend
   ```

3. Apply any database migrations:
   ```
   docker-compose exec backend flask db upgrade
   ```

### Frontend Updates

1. Pull the latest code:
   ```
   git pull origin main
   ```

2. Rebuild and restart the frontend container:
   ```
   docker-compose build frontend
   docker-compose up -d frontend
   ```

## Monitoring and Logs

### Viewing Logs

1. View logs for all services:
   ```
   docker-compose logs
   ```

2. View logs for a specific service:
   ```
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. Follow logs in real-time:
   ```
   docker-compose logs -f
   ```

### Common Issues and Troubleshooting

#### Backend Issues

1. **Database connection errors**:
   - Check if the database file exists
   - Verify permissions on the database file
   - Solution: `docker-compose exec backend ls -la instance/`

2. **API errors**:
   - Check backend logs for specific error messages
   - Solution: `docker-compose logs backend`

3. **Database migration errors**:
   - Check migration files in the `migrations` directory
   - Try downgrading and upgrading again
   - Solution: 
     ```
     docker-compose exec backend flask db downgrade
     docker-compose exec backend flask db upgrade
     ```

#### Frontend Issues

1. **API connection errors**:
   - Verify the `REACT_APP_API_URL` is set correctly
   - Check if the backend is running and accessible
   - Solution: Check network settings in docker-compose.yml

2. **Build errors**:
   - Check for dependency issues
   - Solution: 
     ```
     docker-compose exec frontend npm install
     docker-compose restart frontend
     ```

3. **Blank screen or UI errors**:
   - Check browser console for JavaScript errors
   - Solution: Check frontend logs and rebuild if necessary

## Performance Optimization

### Backend Optimization

1. Enable production mode:
   ```
   # In docker-compose.yml
   environment:
     - FLASK_ENV=production
     - FLASK_DEBUG=0
   ```

2. Add database indexes for frequently queried fields:
   - Modify models to include indexes
   - Create a migration to add the indexes

### Frontend Optimization

1. Build for production:
   ```
   # In frontend Dockerfile
   RUN npm run build
   ```

2. Serve static files from a CDN or web server:
   - Configure a web server like Nginx to serve the built frontend files

## Security Maintenance

1. Keep dependencies updated:
   ```
   # Update backend dependencies
   docker-compose exec backend pip install --upgrade -r requirements.txt
   
   # Update frontend dependencies
   docker-compose exec frontend npm update
   ```

2. Regularly back up the database

3. Implement proper authentication (for future enhancements)

4. Set proper CORS headers in the backend configuration

## Scaling the Application

For larger deployments:

1. Consider moving from SQLite to a more robust database like PostgreSQL

2. Implement a proper web server (Nginx, Apache) in front of the Flask application

3. Use a process manager like Gunicorn for the backend

4. Implement caching for frequently accessed data

5. Consider containerizing with Kubernetes for more advanced scaling