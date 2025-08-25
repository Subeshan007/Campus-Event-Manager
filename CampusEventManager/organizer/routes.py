from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import data_store, Event, User
from utils import login_required, send_notification
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

organizer_bp = Blueprint('organizer', __name__)

@organizer_bp.route('/dashboard')
@login_required('organizer')
def dashboard():
    user_id = session['user_id']
    
    # Get organizer's events
    organizer_events = []
    for event_id, event in data_store.events.items():
        if event['organizer_id'] == user_id:
            # Count registrations for this event
            registrations = sum(1 for reg in data_store.registrations.values() 
                              if reg['event_id'] == event_id)
            event_with_stats = event.copy()
            event_with_stats['registrations'] = registrations
            organizer_events.append(event_with_stats)
    
    # Sort by created date
    organizer_events.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Statistics
    total_events = len(organizer_events)
    approved_events = len([e for e in organizer_events if e['status'] == 'approved'])
    pending_events = len([e for e in organizer_events if e['status'] == 'pending'])
    total_registrations = sum(e['registrations'] for e in organizer_events)
    
    stats = {
        'total_events': total_events,
        'approved_events': approved_events,
        'pending_events': pending_events,
        'total_registrations': total_registrations
    }
    
    return render_template('organizer/dashboard.html', 
                         events=organizer_events[:5],  # Show latest 5
                         stats=stats)

@organizer_bp.route('/create-event', methods=['GET', 'POST'])
@login_required('organizer')
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        venue = request.form['venue']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        category = request.form['category']
        max_attendees = request.form.get('max_attendees')
        is_paid = 'is_paid' in request.form
        
        # --- START: CORRECTED CODE ---
        price_string = request.form.get('price', '').strip()
        if price_string:
            try:
                price = float(price_string)
            except ValueError:
                price = 0.0
        else:
            price = 0.0
        # --- END: CORRECTED CODE ---
        
        if max_attendees:
            max_attendees = int(max_attendees)
        
        # Validation
        if start_date >= end_date:
            flash('End date must be after start date', 'error')
            return render_template('organizer/create_event.html')
        
        if start_date <= datetime.now():
            flash('Start date must be in the future', 'error')
            return render_template('organizer/create_event.html')
        
        # Create event
        event = Event(title, description, session['user_id'], venue, 
                     start_date, end_date, category, max_attendees)
        event.is_paid = is_paid
        event.price = price
        
        # Handle team participation
        participation_type = request.form.get('participation_type', 'individual')
        event.is_competition = (participation_type == 'team')
        
        if event.is_competition:
            team_size_min = request.form.get('team_size_min')
            team_size_max = request.form.get('team_size_max')
            if team_size_min:
                event.team_size_min = int(team_size_min)
            if team_size_max:
                event.team_size_max = int(team_size_max)
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(f"{event.id}_{file.filename}")
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                event.image_path = f"uploads/{filename}"
        
        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'organizer_id': event.organizer_id,
            'venue': event.venue,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'category': event.category,
            'max_attendees': event.max_attendees,
            'current_attendees': event.current_attendees,
            'status': event.status,
            'created_at': event.created_at,
            'image_path': event.image_path,
            'is_paid': event.is_paid,
            'price': event.price,
            'is_competition': event.is_competition,
            'team_size_min': event.team_size_min,
            'team_size_max': event.team_size_max
        }
        
        data_store.add_event(event.id, event_data)
        
        flash('Event created successfully and submitted for approval!', 'success')
        return redirect(url_for('organizer.manage_events'))
    
    return render_template('organizer/create_event.html')

@organizer_bp.route('/manage-events')
@login_required('organizer')
def manage_events():
    user_id = session['user_id']
    
    # Get organizer's events with registration stats
    organizer_events = []
    for event_id, event in data_store.events.items():
        if event['organizer_id'] == user_id:
            # Count registrations
            registrations = []
            for reg_id, reg in data_store.registrations.items():
                if reg['event_id'] == event_id:
                    user = data_store.users.get(reg['user_id'], {})
                    registrations.append({
                        'registration': reg,
                        'user': user
                    })
            
            event_with_regs = event.copy()
            event_with_regs['registrations'] = registrations
            organizer_events.append(event_with_regs)
    
    # Sort by created date
    organizer_events.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('organizer/manage_events.html', events=organizer_events)

@organizer_bp.route('/event-analytics/<event_id>')
@login_required('organizer')
def event_analytics(event_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Event not found', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    # Get registrations with user details
    registrations = []
    for reg_id, reg in data_store.registrations.items():
        if reg['event_id'] == event_id:
            user = data_store.users.get(reg['user_id'], {})
            registrations.append({
                'registration': reg,
                'user': user
            })
    
    # Get feedback for this event
    event_feedback = []
    total_rating = 0
    for fb_id, fb in data_store.feedback.items():
        if fb['event_id'] == event_id:
            user = data_store.users.get(fb['user_id'], {})
            event_feedback.append({
                'feedback': fb,
                'user': user
            })
            total_rating += fb['rating']
    
    avg_rating = total_rating / len(event_feedback) if event_feedback else 0
    
    # Calculate statistics
    stats = {
        'total_registrations': len(registrations),
        'attended': len([r for r in registrations if r['registration']['attended']]),
        'feedback_count': len(event_feedback),
        'avg_rating': round(avg_rating, 2),
        'attendance_rate': round((len([r for r in registrations if r['registration']['attended']]) / len(registrations) * 100) if registrations else 0, 2)
    }
    
    return render_template('organizer/event_analytics.html',
                         event=event,
                         registrations=registrations,
                         feedback=event_feedback,
                         stats=stats)

@organizer_bp.route('/mark-attendance/<event_id>/<reg_id>', methods=['POST'])
@login_required('organizer')
def mark_attendance(event_id, reg_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    registration = data_store.registrations.get(reg_id)
    if registration and registration['event_id'] == event_id:
        registration['attended'] = not registration['attended']
        data_store.save_data()  # Save after updating attendance
        status = 'marked as attended' if registration['attended'] else 'marked as not attended'
        flash(f'Participant {status}', 'success')
    else:
        flash('Registration not found', 'error')
    
    return redirect(url_for('organizer.event_analytics', event_id=event_id))

@organizer_bp.route('/delete-event/<event_id>', methods=['POST'])
@login_required('organizer')
def delete_event(event_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    if event['status'] == 'approved' and event['current_attendees'] > 0:
        flash('Cannot delete event with registered participants. Use Cancel or Force Delete options.', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    # Delete event and related data
    data_store.delete_event(event_id)
    
    # Delete registrations
    regs_to_delete = [reg_id for reg_id, reg in data_store.registrations.items() 
                      if reg['event_id'] == event_id]
    for reg_id in regs_to_delete:
        del data_store.registrations[reg_id]
    
    # Delete feedback
    feedback_to_delete = [fb_id for fb_id, fb in data_store.feedback.items() 
                         if fb['event_id'] == event_id]
    for fb_id in feedback_to_delete:
        del data_store.feedback[fb_id]
    
    # Delete teams and submissions for this event
    teams_to_delete = [team_id for team_id, team in data_store.teams.items() 
                      if team['event_id'] == event_id]
    for team_id in teams_to_delete:
        del data_store.teams[team_id]
    
    submissions_to_delete = [sub_id for sub_id, sub in data_store.submissions.items() 
                           if sub['event_id'] == event_id]
    for sub_id in submissions_to_delete:
        del data_store.submissions[sub_id]
    
    # Save data after deletions
    data_store.save_data()
    
    flash('Event deleted successfully', 'success')
    return redirect(url_for('organizer.manage_events'))

@organizer_bp.route('/cancel-event/<event_id>', methods=['POST'])
@login_required('organizer')
def cancel_event(event_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    # Update event status to cancelled
    event['status'] = 'cancelled'
    event['cancelled_at'] = datetime.now()
    
    # Notify all registered participants
    registered_users = []
    for reg in data_store.registrations.values():
        if reg['event_id'] == event_id:
            user = data_store.users.get(reg['user_id'])
            if user:
                registered_users.append(user)
                send_notification(user['id'], 'Event Cancelled', 
                                f'The event "{event["title"]}" has been cancelled by the organizer.')
    
    data_store.save_data()
    
    flash(f'Event cancelled successfully. {len(registered_users)} participants have been notified.', 'warning')
    return redirect(url_for('organizer.manage_events'))

@organizer_bp.route('/force-delete-event/<event_id>', methods=['POST'])
@login_required('organizer')
def force_delete_event(event_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    # Count affected participants
    registered_count = len([reg for reg in data_store.registrations.values() 
                           if reg['event_id'] == event_id])
    
    # Notify all registered participants before deletion
    for reg in data_store.registrations.values():
        if reg['event_id'] == event_id:
            user = data_store.users.get(reg['user_id'])
            if user:
                send_notification(user['id'], 'Event Deleted', 
                                f'The event "{event["title"]}" has been permanently deleted by the organizer.')
    
    # Delete event and all related data
    data_store.delete_event(event_id)
    
    # Delete registrations
    regs_to_delete = [reg_id for reg_id, reg in data_store.registrations.items() 
                      if reg['event_id'] == event_id]
    for reg_id in regs_to_delete:
        del data_store.registrations[reg_id]
    
    # Delete feedback
    feedback_to_delete = [fb_id for fb_id, fb in data_store.feedback.items() 
                         if fb['event_id'] == event_id]
    for fb_id in feedback_to_delete:
        del data_store.feedback[fb_id]
    
    # Delete teams and submissions for this event
    teams_to_delete = [team_id for team_id, team in data_store.teams.items() 
                      if team['event_id'] == event_id]
    for team_id in teams_to_delete:
        del data_store.teams[team_id]
    
    submissions_to_delete = [sub_id for sub_id, sub in data_store.submissions.items() 
                           if sub['event_id'] == event_id]
    for sub_id in submissions_to_delete:
        del data_store.submissions[sub_id]
    
    # Save data after deletions
    data_store.save_data()
    
    flash(f'Event permanently deleted. {registered_count} participants were notified.', 'success')
    return redirect(url_for('organizer.manage_events'))

@organizer_bp.route('/team-submissions/<event_id>')
@login_required('organizer')
def team_submissions(event_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Event not found or unauthorized', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    if not event.get('is_competition', False):
        flash('This event is not a team competition', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    # Get all submissions for this event
    event_submissions = []
    for submission in data_store.submissions.values():
        if submission['event_id'] == event_id:
            team = data_store.teams.get(submission['team_id'])
            if team:
                # Get team members
                team_members = []
                for member_id in team['members']:
                    member = data_store.users.get(member_id)
                    if member:
                        team_members.append(member)
                
                event_submissions.append({
                    'submission': submission,
                    'team': team,
                    'team_members': team_members
                })
    
    # Sort by submission date
    event_submissions.sort(key=lambda x: x['submission']['submitted_at'], reverse=True)
    
    return render_template('organizer/team_submissions.html', 
                         event=event, 
                         submissions=event_submissions)

@organizer_bp.route('/evaluate-submission/<submission_id>', methods=['GET', 'POST'])
@login_required('organizer')
def evaluate_submission(submission_id):
    submission = data_store.submissions.get(submission_id)
    if not submission:
        flash('Submission not found', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    event = data_store.events.get(submission['event_id'])
    if not event or event['organizer_id'] != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    if request.method == 'POST':
        score = float(request.form['score'])
        feedback = request.form.get('feedback', '')
        
        # Update submission
        submission['score'] = score
        submission['status'] = 'evaluated'
        submission['feedback'] = feedback
        
        # Calculate ranks for all evaluated submissions in this event
        event_submissions = [s for s in data_store.submissions.values() 
                           if s['event_id'] == submission['event_id'] and s['status'] == 'evaluated']
        event_submissions.sort(key=lambda x: x['score'], reverse=True)
        
        for i, sub in enumerate(event_submissions):
            sub['rank'] = i + 1
        
        data_store.save_data()
        
        flash('Submission evaluated successfully!', 'success')
        return redirect(url_for('organizer.team_submissions', event_id=submission['event_id']))
    
    team = data_store.teams.get(submission['team_id'])
    team_members = []
    if team:
        for member_id in team['members']:
            member = data_store.users.get(member_id)
            if member:
                team_members.append(member)
    
    return render_template('organizer/evaluate_submission.html',
                         submission=submission,
                         team=team,
                         team_members=team_members,
                         event=event)

@organizer_bp.route('/announce-results/<event_id>', methods=['GET', 'POST'])
@login_required('organizer')
def announce_results(event_id):
    event = data_store.events.get(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash('Event not found or unauthorized', 'error')
        return redirect(url_for('organizer.manage_events'))
    
    if request.method == 'POST':
        # Mark results as announced
        event['results_announced'] = True
        event['results_announcement_date'] = datetime.now()
        data_store.save_data()
        
        flash('Results announced successfully!', 'success')
        return redirect(url_for('organizer.team_submissions', event_id=event_id))
    
    # Get evaluated submissions
    evaluated_submissions = []
    for submission in data_store.submissions.values():
        if submission['event_id'] == event_id and submission['status'] == 'evaluated':
            team = data_store.teams.get(submission['team_id'])
            if team:
                evaluated_submissions.append({
                    'submission': submission,
                    'team': team
                })
    
    # Sort by rank
    evaluated_submissions.sort(key=lambda x: x['submission']['rank'])
    
    return render_template('organizer/announce_results.html',
                         event=event,
                         submissions=evaluated_submissions)

@organizer_bp.route('/register-organizer', methods=['GET', 'POST'])
def register_organizer():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        department = request.form['department']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('organizer/register_organizer.html')
        
        # Check if email already exists
        for uid, user in data_store.users.items():
            if user['email'] == email:
                flash('Email already registered', 'error')
                return render_template('organizer/register_organizer.html')
        
        # Create new organizer
        user = User(username, email, generate_password_hash(password), 'organizer')
        data_store.users[user.id] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'role': user.role,
            'created_at': user.created_at,
            'is_active': user.is_active,
            'department': department
        }
        
        flash('Organizer registration successful! Please login.', 'success')
        return redirect(url_for('auth.organizer_login'))
    
    return render_template('organizer/register_organizer.html')