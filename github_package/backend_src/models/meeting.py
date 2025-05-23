from datetime import datetime
from src.models.user import db

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('Participant', backref='meeting', lazy=True, cascade="all, delete-orphan")
    chat_messages = db.relationship('ChatMessage', backref='meeting', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Meeting {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    join_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leave_time = db.Column(db.DateTime)
    speaking_time = db.Column(db.Integer, default=0)  # in seconds
    engagement_score = db.Column(db.Float, default=0.0)
    
    # Relationships
    voice_activities = db.relationship('VoiceActivity', backref='participant', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Participant {self.user_id} in Meeting {self.meeting_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'user_id': self.user_id,
            'join_time': self.join_time.isoformat() if self.join_time else None,
            'leave_time': self.leave_time.isoformat() if self.leave_time else None,
            'speaking_time': self.speaking_time,
            'engagement_score': self.engagement_score
        }


class VoiceActivity(db.Model):
    __tablename__ = 'voice_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer, default=0)  # in seconds
    
    def __repr__(self):
        return f'<VoiceActivity {self.id} by Participant {self.participant_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration
        }


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id} by User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'user_id': self.user_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }


class DocumentActivity(db.Model):
    __tablename__ = 'document_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_id = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # edit, comment, view
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DocumentActivity {self.id} by User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'activity_type': self.activity_type,
            'timestamp': self.timestamp.isoformat()
        }


class TaskActivity(db.Model):
    __tablename__ = 'task_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # create, update, complete
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TaskActivity {self.id} by User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'activity_type': self.activity_type,
            'timestamp': self.timestamp.isoformat()
        }
