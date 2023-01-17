from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    public_id = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    user_address = db.Column(db.String(100), nullable=True)
    login_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.email

# Listing model
class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=False)
    location_address = db.Column(db.String(100), nullable=False)
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return '<Listing %r>' % self.id