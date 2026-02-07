from app import db
from datetime import datetime
from flask_login import UserMixin

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team = db.relationship('Team', backref=db.backref('users', lazy=True))
    meetings = db.relationship('Meeting', secondary='participants_user', backref=db.backref('participants', lazy='dynamic'))

# Team model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Room model
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.Text)
    location = db.Column(db.String(100))
    availability = db.Column(db.Boolean, default=True)

# Meeting model
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='scheduled')
    cost = db.Column(db.Float, default=0.0)
    
    # Relationships
    room = db.relationship('Room', backref=db.backref('meetings', lazy=True))
    organizer = db.relationship('User', backref=db.backref('organized_meetings', lazy=True))
    cost_logs = db.relationship('CostLog', backref=db.backref('meeting', lazy=True))
    partners = db.relationship('Businesspartner', secondary='participants_partner', backref=db.backref('meetings', lazy='dynamic'))

# CostLog model
class CostLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationship
    submitter = db.relationship('User', backref=db.backref('submitted_costs', lazy=True))

# Businesspartner model
class Businesspartner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)

# Association tables
participants_user = db.Table('participants_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
)

participants_partner = db.Table('participants_partner',
    db.Column('partner_id', db.Integer, db.ForeignKey('businesspartner.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
)