"""
Base model with common fields and functionality.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model with common fields."""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def save(self):
        """Save model to database."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete model from database."""
        db.session.delete(self)
        db.session.commit()
        return True
