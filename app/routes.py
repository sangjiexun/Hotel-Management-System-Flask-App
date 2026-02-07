from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from app.models import User, Team, Room, Meeting, CostLog, Participants_user, Participants_partner, Businesspartner
from app.forms import LoginForm, RegistrationForm, RoomForm, MeetingForm, TeamForm, CostLogForm, BusinessPartnerForm
from datetime import datetime, timedelta

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # In production, use hashed passwords
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    # Populate team choices
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # In production, use hashed passwords
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            team_id=form.team_id.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Index route
@app.route('/index')
@login_required
def index():
    # Get upcoming meetings for the current user
    upcoming_meetings = Meeting.query.join(Participants_user).filter(
        Participants_user.c.user_id == current_user.id,
        Meeting.start_time > datetime.utcnow()
    ).order_by(Meeting.start_time).limit(5).all()
    
    return render_template('index.html', title='Home', meetings=upcoming_meetings)

# Room booking route
@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = MeetingForm()
    
    # Populate room choices
    form.room_id.choices = [(room.id, room.name) for room in Room.query.filter_by(availability=True).all()]
    
    # Populate participant choices
    participants = User.query.all()
    form.participants.choices = [(user.id, f'{user.first_name} {user.last_name}') for user in participants]
    
    # Populate business partner choices
    partners = Businesspartner.query.all()
    form.partners.choices = [(partner.id, partner.name) for partner in partners]
    
    if form.validate_on_submit():
        # Create meeting datetime
        start_datetime = datetime.combine(form.date.data, form.start_time.data)
        end_datetime = datetime.combine(form.date.data, form.end_time.data)
        
        # Check if room is available
        overlapping_meetings = Meeting.query.filter(
            Meeting.room_id == form.room_id.data,
            Meeting.start_time < end_datetime,
            Meeting.end_time > start_datetime
        ).all()
        
        if overlapping_meetings:
            flash('Room is not available for the selected time', 'danger')
            return redirect(url_for('book'))
        
        # Create meeting
        meeting = Meeting(
            title=form.title.data,
            description=form.description.data,
            start_time=start_datetime,
            end_time=end_datetime,
            room_id=form.room_id.data,
            organizer_id=current_user.id
        )
        db.session.add(meeting)
        db.session.commit()
        
        # Add participants
        for participant_id in request.form.getlist('participants'):
            participant = Participants_user.insert().values(
                user_id=participant_id,
                meeting_id=meeting.id
            )
            db.session.execute(participant)
        
        # Add business partners
        for partner_id in request.form.getlist('partners'):
            partner = Participants_partner.insert().values(
                partner_id=partner_id,
                meeting_id=meeting.id
            )
            db.session.execute(partner)
        
        db.session.commit()
        flash('Meeting has been scheduled', 'success')
        return redirect(url_for('index'))
    
    return render_template('book.html', title='Book Room', form=form)

# Room availability route
@app.route('/roomavailable')
@login_required
def roomavailable():
    # Get today's date
    today = datetime.utcnow().date()
    
    # Get available rooms
    available_rooms = Room.query.filter_by(availability=True).all()
    
    return render_template('roomavailable.html', title='Room Availability', rooms=available_rooms, today=today)

# Room availability list route
@app.route('/roomavailablelist', methods=['GET', 'POST'])
@login_required
def roomavailablelist():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        
        # Create datetime objects
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        
        # Get all rooms
        all_rooms = Room.query.filter_by(availability=True).all()
        
        # Check availability for each room
        available_rooms = []
        for room in all_rooms:
            overlapping_meetings = Meeting.query.filter(
                Meeting.room_id == room.id,
                Meeting.start_time < end_datetime,
                Meeting.end_time > start_datetime
            ).all()
            
            if not overlapping_meetings:
                available_rooms.append(room)
        
        return render_template('roomavailablelist.html', title='Available Rooms', rooms=available_rooms, date=date, start_time=start_time, end_time=end_time)
    
    return render_template('roomavailable.html', title='Room Availability')

# Room occupation route
@app.route('/roomoccupation')
@login_required
def roomoccupation():
    # Get today's date
    today = datetime.utcnow().date()
    
    # Get all rooms
    rooms = Room.query.all()
    
    return render_template('roomoccupation.html', title='Room Occupation', rooms=rooms, today=today)

# Room occupation list route
@app.route('/roomoccupationlist', methods=['GET', 'POST'])
@login_required
def roomoccupationlist():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        # Get all rooms
        rooms = Room.query.all()
        
        # Get meetings for each room on the selected date
        room_meetings = {}
        for room in rooms:
            meetings = Meeting.query.filter(
                Meeting.room_id == room.id,
                Meeting.start_time >= datetime.combine(date, datetime.min.time()),
                Meeting.start_time <= datetime.combine(date, datetime.max.time())
            ).order_by(Meeting.start_time).all()
            room_meetings[room.id] = meetings
        
        return render_template('roomoccupationlist.html', title='Room Occupation', rooms=rooms, room_meetings=room_meetings, date=date)
    
    return render_template('roomoccupation.html', title='Room Occupation')

# Cost management route
@app.route('/costs')
@login_required
def costs():
    # Get all meetings with costs
    meetings = Meeting.query.filter(Meeting.cost > 0).all()
    
    return render_template('costs.html', title='Cost Management', meetings=meetings)

# Cost check route
@app.route('/costcheck/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def costcheck(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    form = CostLogForm()
    
    if form.validate_on_submit():
        # Add cost log
        cost_log = CostLog(
            meeting_id=meeting_id,
            description=form.description.data,
            amount=form.amount.data,
            submitted_by=current_user.id
        )
        db.session.add(cost_log)
        
        # Update meeting cost
        meeting.cost += form.amount.data
        
        db.session.commit()
        flash('Cost has been added', 'success')
        return redirect(url_for('costcheck', meeting_id=meeting_id))
    
    # Get cost logs for this meeting
    cost_logs = CostLog.query.filter_by(meeting_id=meeting_id).all()
    
    return render_template('costcheck.html', title='Cost Details', meeting=meeting, form=form, cost_logs=cost_logs)

# Team management route
@app.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():
    form = TeamForm()
    
    if form.validate_on_submit():
        team = Team(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(team)
        db.session.commit()
        flash('Team has been created', 'success')
        return redirect(url_for('teams'))
    
    # Get all teams
    teams = Team.query.all()
    
    return render_template('teams.html', title='Team Management', form=form, teams=teams)

# Add team route
@app.route('/addteam', methods=['GET', 'POST'])
@login_required
def addteam():
    form = TeamForm()
    
    if form.validate_on_submit():
        team = Team(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(team)
        db.session.commit()
        flash('Team has been created', 'success')
        return redirect(url_for('teams'))
    
    return render_template('addteam.html', title='Add Team', form=form)

# Delete team route
@app.route('/deleteteam/<int:team_id>')
@login_required
def deleteteam(team_id):
    team = Team.query.get_or_404(team_id)
    
    # Check if team has users
    if team.users:
        flash('Cannot delete team with users', 'danger')
        return redirect(url_for('teams'))
    
    db.session.delete(team)
    db.session.commit()
    flash('Team has been deleted', 'success')
    return redirect(url_for('teams'))

# User management route
@app.route('/users')
@login_required
def users():
    # Get all users
    users = User.query.all()
    
    return render_template('users.html', title='User Management', users=users)

# Add user route
@app.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    form = RegistrationForm()
    # Populate team choices
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # In production, use hashed passwords
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            team_id=form.team_id.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User has been created', 'success')
        return redirect(url_for('users'))
    
    return render_template('adduser.html', title='Add User', form=form)

# Delete user route
@app.route('/deleteuser/<int:user_id>')
@login_required
def deleteuser(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if user is organizer of any meetings
    if user.organized_meetings:
        flash('Cannot delete user who is organizer of meetings', 'danger')
        return redirect(url_for('users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('users'))

# All records route
@app.route('/allrecords')
@login_required
def allrecords():
    # Get all meetings
    meetings = Meeting.query.order_by(Meeting.start_time.desc()).all()
    
    return render_template('allrecords.html', title='All Meetings', meetings=meetings)

# Cancel booking route
@app.route('/cancelbooking/<int:meeting_id>')
@login_required
def cancelbooking(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Check if current user is the organizer
    if meeting.organizer_id != current_user.id:
        flash('Only the organizer can cancel the meeting', 'danger')
        return redirect(url_for('allrecords'))
    
    # Update meeting status
    meeting.status = 'cancelled'
    db.session.commit()
    flash('Meeting has been cancelled', 'success')
    return redirect(url_for('allrecords'))