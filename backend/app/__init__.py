import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    """Create and configure the Flask app"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///notscrum.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register API blueprints
    from .api import boards, lanes, cards
    app.register_blueprint(boards.bp)
    app.register_blueprint(lanes.bp)
    app.register_blueprint(cards.bp)
    
    # Configure Swagger UI
    from .api.swagger import configure_swagger
    configure_swagger(app)
    
    return app