from app import db
from datetime import datetime

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(20), default='white')  # For color-coding cards
    position = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    lane_id = db.Column(db.Integer, db.ForeignKey('lane.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'color': self.color,
            'position': self.position,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'lane_id': self.lane_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
    def __repr__(self):
        return f'<Card {self.title}>'