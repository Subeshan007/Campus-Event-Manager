from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import data_store, Registration, Feedback
from utils import login_required, send_notification, generate_qr_code
from datetime import datetime, timedelta

student_bp = Blueprint('student', __name__)

# Import and register team routes
from student.team_routes import team_bp
student_bp.register_blueprint(team_bp, url_prefix='/team')

@student_bp.route('/dashboard')
@login_required('student')
def dashboard():
    user_id = session['user_id']

    # Get upcoming events (approved only)
    upcoming_events = []
    for event_id, event in data_store.events.items():
        if event['status'] == 'approved':
            # Ensure start_date is a datetime object
            start_date = event['start_date']
            if isinstance(start_date, str):
                try:
                    start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                except:
                    continue

            if isinstance(start_date, datetime) and start_date > datetime.now():
                upcoming_events.append(event)

    # Sort by start date
    def get_sort_date(event):
        start_date = event['start_date']
        if isinstance(start_date, str):
            try:
                return datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except:
                return datetime.min
        return start_date if isinstance(start_date, datetime) else datetime.min

    upcoming_events.sort(key=get_sort_date)
    upcoming_events = upcoming_events[:6]  # Show only 6 events

    # Get user's registered events
    user_registrations = []
    for reg_id, reg in data_store.registrations.items():
        if reg['user_id'] == user_id:
            event = data_store.events.get(reg['event_id'])
            if event:
                user_registrations.append({
                    'registration': reg,
                    'event': event
                })

    return render_template('student/dashboard.html', 
                         upcoming_events=upcoming_events,
                         user_registrations=user_registrations,
                         datetime=datetime) # <-- ADD THIS LINE

@student_bp.route('/events')
@login_required('student')
def events():
    # Get all approved events
    approved_events = []
    for event_id, event in data_store.events.items():
        if event['status'] == 'approved':
            approved_events.append(event)

    # Apply filters
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    date_filter = request.args.get('date', '')

    if category:
        approved_events = [e for e in approved_events if e['category'] == category]

    if search:
        search_lower = search.lower()
        approved_events = [e for e in approved_events if 
                          search_lower in e['title'].lower() or 
                          search_lower in e['description'].lower()]

    if date_filter:
        if date_filter == 'today':
            today = datetime.now().date()
            filtered_events = []
            for e in approved_events:
                start_date = e['start_date']
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    except:
                        continue
                if isinstance(start_date, datetime) and start_date.date() == today:
                    filtered_events.append(e)
            approved_events = filtered_events
        elif date_filter == 'this_week':
            week_start = datetime.now().date()
            week_end = week_start + timedelta(days=7)
            filtered_events = []
            for e in approved_events:
                start_date = e['start_date']
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    except:
                        continue
                if isinstance(start_date, datetime) and week_start <= start_date.date() <= week_end:
                    filtered_events.append(e)
            approved_events = filtered_events
        elif date_filter == 'this_month':
            month_start = datetime.now().replace(day=1).date()
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1) - timedelta(days=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1) - timedelta(days=1)
            filtered_events = []
            for e in approved_events:
                start_date = e['start_date']
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    except:
                        continue
                if isinstance(start_date, datetime) and month_start <= start_date.date() <= month_end:
                    filtered_events.append(e)
            approved_events = filtered_events

    # Sort by start date
    def get_sort_date(event):
        start_date = event['start_date']
        if isinstance(start_date, str):
            try:
                return datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except:
                return datetime.min
        return start_date if isinstance(start_date, datetime) else datetime.min

    approved_events.sort(key=get_sort_date)

    # Get unique categories for filter
    categories = list(set([e['category'] for e in data_store.events.values() if e['status'] == 'approved']))

    return render_template('student/events.html', 
                         events=approved_events,
                         categories=categories,
                         current_filters={
                             'category': category,
                             'search': search,
                             'date': date_filter
                         })

@student_bp.route('/event/<event_id>')
@login_required('student')
def event_detail(event_id):
    event = data_store.events.get(event_id)
    if not event or event['status'] != 'approved':
        flash('Event not found', 'error')
        return redirect(url_for('student.events'))

    # Check if user is already registered
    user_id = session['user_id']
    is_registered = False
    registration = None

    for reg_id, reg in data_store.registrations.items():
        if reg['user_id'] == user_id and reg['event_id'] == event_id:
            is_registered = True
            registration = reg
            break

    # Get organizer info
    organizer = data_store.users.get(event['organizer_id'], {})

    # Get event feedback
    event_feedback = []
    for fb_id, fb in data_store.feedback.items():
        if fb['event_id'] == event_id:
            user = data_store.users.get(fb['user_id'], {})
            event_feedback.append({
                'feedback': fb,
                'user': user
            })

    # Get all teams for this user (needed for template logic)
    user_teams = []
    for team in data_store.teams.values():
        if user_id in team['members']:
            user_teams.append(team)

    return render_template('student/event_detail.html',
                         event=event,
                         organizer=organizer,
                         is_registered=is_registered,
                         registration=registration,
                         feedback=event_feedback,
                         user_teams=user_teams,
                         datetime=datetime) # <-- ADD THIS LINE

@student_bp.route('/register/<event_id>', methods=['POST'])
@login_required('student')
def register_event(event_id):
    event = data_store.events.get(event_id)
    if not event or event['status'] != 'approved':
        flash('Event not found', 'error')
        return redirect(url_for('student.events'))

    user_id = session['user_id']

    # Check if already registered
    for reg_id, reg in data_store.registrations.items():
        if reg['user_id'] == user_id and reg['event_id'] == event_id:
            flash('You are already registered for this event', 'warning')
            return redirect(url_for('student.event_detail', event_id=event_id))

    # For team events, check if user is part of a team
    if event.get('is_competition', False):
        user_team = None
        for team in data_store.teams.values():
            if user_id in team['members'] and team['event_id'] == event_id and team['status'] == 'active':
                user_team = team
                break
        
        if not user_team:
            flash('You must create or join a team before registering for this team event', 'error')
            return redirect(url_for('student.event_detail', event_id=event_id))

        # For team events, register all team members
        for member_id in user_team['members']:
            # Check if member is already registered
            already_registered = False
            for reg_id, reg in data_store.registrations.items():
                if reg['user_id'] == member_id and reg['event_id'] == event_id:
                    already_registered = True
                    break
            
            if not already_registered:
                # Create registration for team member
                registration = Registration(member_id, event_id)
                qr_data = f"SMVEC_EVENT_{event_id}_{registration.id}_{member_id}"
                qr_code_image = generate_qr_code(qr_data)

                data_store.registrations[registration.id] = {
                    'id': registration.id,
                    'user_id': registration.user_id,
                    'event_id': registration.event_id,
                    'registered_at': registration.registered_at,
                    'attended': registration.attended,
                    'qr_code': qr_code_image
                }

        # Update event attendee count by team size
        team_size = len(user_team['members'])
        event['current_attendees'] += team_size

        flash(f'Team "{user_team["name"]}" successfully registered for the event!', 'success')
    else:
        # Check capacity for individual events
        if event['max_attendees'] and event['current_attendees'] >= event['max_attendees']:
            flash('Event is full', 'error')
            return redirect(url_for('student.event_detail', event_id=event_id))

        # Create registration for individual event
        registration = Registration(user_id, event_id)

        # Generate QR code with registration details
        qr_data = f"SMVEC_EVENT_{event_id}_{registration.id}_{user_id}"
        qr_code_image = generate_qr_code(qr_data)

        data_store.registrations[registration.id] = {
            'id': registration.id,
            'user_id': registration.user_id,
            'event_id': registration.event_id,
            'registered_at': registration.registered_at,
            'attended': registration.attended,
            'qr_code': qr_code_image
        }

        # Update event attendee count
        event['current_attendees'] += 1

        flash('Successfully registered for the event!', 'success')

    # Save data
    data_store.save_data()

    # Send notification
    send_notification(user_id, 'Registration Successful', 
                     f'You have successfully registered for {event["title"]}')

    return redirect(url_for('student.event_detail', event_id=event_id))

@student_bp.route('/unregister/<event_id>', methods=['POST'])
@login_required('student')
def unregister_event(event_id):
    user_id = session['user_id']

    # Find and remove registration
    reg_to_remove = None
    for reg_id, reg in data_store.registrations.items():
        if reg['user_id'] == user_id and reg['event_id'] == event_id:
            reg_to_remove = reg_id
            break

    if reg_to_remove:
        del data_store.registrations[reg_to_remove]

        # Update event attendee count
        event = data_store.events.get(event_id)
        if event and event['current_attendees'] > 0:
            event['current_attendees'] -= 1

        flash('Successfully unregistered from the event', 'info')
    else:
        flash('Registration not found', 'error')

    return redirect(url_for('student.event_detail', event_id=event_id))

@student_bp.route('/my-events')
@login_required('student')
def my_events():
    user_id = session['user_id']

    # Get user's registrations with event details
    registered_events = []
    for reg_id, reg in data_store.registrations.items():
        if reg['user_id'] == user_id:
            event = data_store.events.get(reg['event_id'])
            if event:
                registered_events.append({
                    'registration': reg,
                    'event': event
                })

    # Sort by registration date
    registered_events.sort(key=lambda x: x['registration']['registered_at'], reverse=True)

    # Calculate stats for summary cards
    now = datetime.now()
    upcoming_count = 0
    attended_count = 0

    for item in registered_events:
        # Ensure start_date is a datetime object before comparison
        start_date = item['event']['start_date']
        if isinstance(start_date, datetime) and start_date > now:
            upcoming_count += 1
        if item['registration']['attended']:
            attended_count += 1

    return render_template('student/my_events.html', 
                           registered_events=registered_events,
                           upcoming_count=upcoming_count,
                           attended_count=attended_count,
                           datetime=datetime) # <-- ADD THIS LINE


@student_bp.route('/calendar')
@login_required('student')
def calendar():
    # Get all approved events for calendar view
    approved_events = []
    for event_id, event in data_store.events.items():
        if event['status'] == 'approved':
            approved_events.append(event)

    return render_template('student/calendar.html', events=approved_events)

@student_bp.route('/feedback/<event_id>', methods=['POST'])
@login_required('student')
def submit_feedback(event_id):
    user_id = session['user_id']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    # Check if user attended the event
    attended = False
    for reg_id, reg in data_store.registrations.items():
        if reg['user_id'] == user_id and reg['event_id'] == event_id and reg['attended']:
            attended = True
            break

    if not attended:
        flash('You can only provide feedback for events you attended', 'error')
        return redirect(url_for('student.event_detail', event_id=event_id))

    # Check if feedback already exists
    for fb_id, fb in data_store.feedback.items():
        if fb['user_id'] == user_id and fb['event_id'] == event_id:
            flash('You have already provided feedback for this event', 'warning')
            return redirect(url_for('student.event_detail', event_id=event_id))

    # Create feedback
    feedback = Feedback(user_id, event_id, rating, comment)
    data_store.feedback[feedback.id] = {
        'id': feedback.id,
        'user_id': feedback.user_id,
        'event_id': feedback.event_id,
        'rating': feedback.rating,
        'comment': feedback.comment,
        'created_at': feedback.created_at
    }

    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('student.event_detail', event_id=event_id))