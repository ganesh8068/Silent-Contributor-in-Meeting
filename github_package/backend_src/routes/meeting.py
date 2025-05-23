from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.meeting import Meeting, Participant, VoiceActivity, ChatMessage, DocumentActivity, TaskActivity
from datetime import datetime

meeting_bp = Blueprint('meeting', __name__)

# Meeting endpoints
@meeting_bp.route('/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([meeting.to_dict() for meeting in meetings]), 200

@meeting_bp.route('/meetings/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return jsonify(meeting.to_dict()), 200

@meeting_bp.route('/meetings', methods=['POST'])
def create_meeting():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    meeting = Meeting(
        title=data['title'],
        start_time=datetime.fromisoformat(data['start_time']) if 'start_time' in data else datetime.utcnow(),
        end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data else None,
        description=data.get('description', '')
    )
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 201

@meeting_bp.route('/meetings/<int:meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    data = request.get_json()
    
    if 'title' in data:
        meeting.title = data['title']
    if 'start_time' in data:
        meeting.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        meeting.end_time = datetime.fromisoformat(data['end_time'])
    if 'description' in data:
        meeting.description = data['description']
    
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 200

@meeting_bp.route('/meetings/<int:meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    db.session.delete(meeting)
    db.session.commit()
    
    return jsonify({'message': 'Meeting deleted successfully'}), 200

# Participant endpoints
@meeting_bp.route('/meetings/<int:meeting_id>/participants', methods=['GET'])
def get_participants(meeting_id):
    participants = Participant.query.filter_by(meeting_id=meeting_id).all()
    return jsonify([participant.to_dict() for participant in participants]), 200

@meeting_bp.route('/meetings/<int:meeting_id>/participants', methods=['POST'])
def add_participant(meeting_id):
    data = request.get_json()
    
    if not data or 'user_id' not in data:
        return jsonify({'error': 'User ID is required'}), 400
    
    # Check if meeting exists
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Check if user exists
    user = User.query.get_or_404(data['user_id'])
    
    # Check if participant already exists
    existing_participant = Participant.query.filter_by(
        meeting_id=meeting_id, 
        user_id=data['user_id']
    ).first()
    
    if existing_participant:
        return jsonify({'error': 'Participant already exists in this meeting'}), 400
    
    participant = Participant(
        meeting_id=meeting_id,
        user_id=data['user_id'],
        join_time=datetime.fromisoformat(data['join_time']) if 'join_time' in data else datetime.utcnow()
    )
    
    db.session.add(participant)
    db.session.commit()
    
    return jsonify(participant.to_dict()), 201

# Voice activity endpoints
@meeting_bp.route('/participants/<int:participant_id>/voice-activities', methods=['POST'])
def record_voice_activity(participant_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Data is required'}), 400
    
    # Check if participant exists
    participant = Participant.query.get_or_404(participant_id)
    
    voice_activity = VoiceActivity(
        participant_id=participant_id,
        start_time=datetime.fromisoformat(data['start_time']) if 'start_time' in data else datetime.utcnow(),
        end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data else None,
        duration=data.get('duration', 0)
    )
    
    # Update participant's speaking time
    participant.speaking_time += voice_activity.duration
    
    db.session.add(voice_activity)
    db.session.commit()
    
    return jsonify(voice_activity.to_dict()), 201

# Chat message endpoints
@meeting_bp.route('/meetings/<int:meeting_id>/chat-messages', methods=['GET'])
def get_chat_messages(meeting_id):
    chat_messages = ChatMessage.query.filter_by(meeting_id=meeting_id).all()
    return jsonify([message.to_dict() for message in chat_messages]), 200

@meeting_bp.route('/meetings/<int:meeting_id>/chat-messages', methods=['POST'])
def add_chat_message(meeting_id):
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'content' not in data:
        return jsonify({'error': 'User ID and content are required'}), 400
    
    # Check if meeting exists
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Check if user exists
    user = User.query.get_or_404(data['user_id'])
    
    chat_message = ChatMessage(
        meeting_id=meeting_id,
        user_id=data['user_id'],
        content=data['content'],
        timestamp=datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else datetime.utcnow()
    )
    
    db.session.add(chat_message)
    db.session.commit()
    
    return jsonify(chat_message.to_dict()), 201

# Engagement score calculation endpoint
@meeting_bp.route('/meetings/<int:meeting_id>/calculate-engagement', methods=['POST'])
def calculate_engagement(meeting_id):
    # Check if meeting exists
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Get all participants in the meeting
    participants = Participant.query.filter_by(meeting_id=meeting_id).all()
    
    for participant in participants:
        # Get voice activities
        voice_activities = VoiceActivity.query.filter_by(participant_id=participant.id).all()
        total_speaking_time = sum(activity.duration for activity in voice_activities)
        
        # Get chat messages
        chat_messages = ChatMessage.query.filter_by(
            meeting_id=meeting_id, 
            user_id=participant.user_id
        ).count()
        
        # Get document activities
        document_activities = DocumentActivity.query.filter_by(
            meeting_id=meeting_id, 
            user_id=participant.user_id
        ).count()
        
        # Get task activities
        task_activities = TaskActivity.query.filter_by(
            meeting_id=meeting_id, 
            user_id=participant.user_id
        ).count()
        
        # Calculate engagement score (simple algorithm for demonstration)
        # This can be enhanced with more sophisticated algorithms
        voice_score = min(total_speaking_time / 60, 10)  # Cap at 10 points for speaking
        chat_score = min(chat_messages * 2, 10)  # 2 points per message, cap at 10
        doc_score = min(document_activities * 2, 5)  # 2 points per activity, cap at 5
        task_score = min(task_activities * 3, 5)  # 3 points per activity, cap at 5
        
        # Total score out of 30, normalized to 0-100
        engagement_score = (voice_score + chat_score + doc_score + task_score) * (100 / 30)
        
        # Update participant's engagement score
        participant.engagement_score = engagement_score
    
    db.session.commit()
    
    return jsonify({
        'message': 'Engagement scores calculated successfully',
        'participants': [participant.to_dict() for participant in participants]
    }), 200

# Silent contributor detection endpoint
@meeting_bp.route('/meetings/<int:meeting_id>/silent-contributors', methods=['GET'])
def get_silent_contributors(meeting_id):
    # Check if meeting exists
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Get all participants in the meeting
    participants = Participant.query.filter_by(meeting_id=meeting_id).all()
    
    silent_contributors = []
    for participant in participants:
        # Define a threshold for "silent" (e.g., less than 60 seconds of speaking)
        if participant.speaking_time < 60:
            user = User.query.get(participant.user_id)
            
            # Get chat messages
            chat_messages = ChatMessage.query.filter_by(
                meeting_id=meeting_id, 
                user_id=participant.user_id
            ).count()
            
            # Get document activities
            document_activities = DocumentActivity.query.filter_by(
                meeting_id=meeting_id, 
                user_id=participant.user_id
            ).count()
            
            # Get task activities
            task_activities = TaskActivity.query.filter_by(
                meeting_id=meeting_id, 
                user_id=participant.user_id
            ).count()
            
            silent_contributors.append({
                'participant': participant.to_dict(),
                'user': user.to_dict(),
                'chat_messages': chat_messages,
                'document_activities': document_activities,
                'task_activities': task_activities,
                'engagement_score': participant.engagement_score
            })
    
    return jsonify(silent_contributors), 200
