from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import data_store, User
from utils import login_required, send_notification
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required('admin')
def dashboard():
    # Calculate statistics
    total_users = len([u for u in data_store.users.values() if u['role'] != 'admin'])
    total_events = len(data_store.events)
    pending_events = len([e for e in data_store.events.values() if e['status'] == 'pending'])
    total_registrations = len(data_store.registrations)
    
    # Recent activity
    recent_events = sorted(data_store.events.values(), 
                          key=lambda x: x['created_at'], reverse=True)[:5]
    
    recent_registrations = []
    recent_regs = sorted(data_store.registrations.values(), 
                        key=lambda x: x['registered_at'], reverse=True)[:5]
    for reg in recent_regs:
        user = data_store.users.get(reg['user_id'], {})
        event = data_store.events.get(reg['event_id'], {})
        recent_registrations.append({
            'registration': reg,
            'user': user,
            'event': event
        })
    
    stats = {
        'total_users': total_users,
        'total_events': total_events,
        'pending_events': pending_events,
        'total_registrations': total_registrations
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_events=recent_events,
                         recent_registrations=recent_registrations)

@admin_bp.route('/approve-events')
@login_required('admin')
def approve_events():
    # Get all events with organizer details
    events_with_organizers = []
    for event_id, event in data_store.events.items():
        organizer = data_store.users.get(event['organizer_id'], {})
        events_with_organizers.append({
            'event': event,
            'organizer': organizer
        })
    
    # Sort by status (pending first) and then by creation date
    events_with_organizers.sort(key=lambda x: (
        0 if x['event']['status'] == 'pending' else 1,
        x['event']['created_at']
    ), reverse=True)
    
    return render_template('admin/approve_events.html', 
                         events_with_organizers=events_with_organizers)

@admin_bp.route('/approve-event/<event_id>', methods=['POST'])
@login_required('admin')
def approve_event(event_id):
    event = data_store.events.get(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin.approve_events'))
    
    if event['status'] != 'pending':
        flash('Event is not pending approval', 'warning')
        return redirect(url_for('admin.approve_events'))
    
    event['status'] = 'approved'
    
    # Send notification to organizer
    send_notification(event['organizer_id'], 'Event Approved', 
                     f'Your event "{event["title"]}" has been approved!')
    
    flash('Event approved successfully', 'success')
    return redirect(url_for('admin.approve_events'))

@admin_bp.route('/reject-event/<event_id>', methods=['POST'])
@login_required('admin')
def reject_event(event_id):
    event = data_store.events.get(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin.approve_events'))
    
    if event['status'] != 'pending':
        flash('Event is not pending approval', 'warning')
        return redirect(url_for('admin.approve_events'))
    
    reason = request.form.get('reason', 'No reason provided')
    event['status'] = 'rejected'
    event['rejection_reason'] = reason
    
    # Send notification to organizer
    send_notification(event['organizer_id'], 'Event Rejected', 
                     f'Your event "{event["title"]}" has been rejected. Reason: {reason}')
    
    flash('Event rejected successfully', 'success')
    return redirect(url_for('admin.approve_events'))

@admin_bp.route('/user-management')
@login_required('admin')
def user_management():
    # Get all users except admins
    users = [u for u in data_store.users.values() if u['role'] != 'admin']
    
    # Sort by creation date
    users.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('admin/user_management.html', users=users)

@admin_bp.route('/create-organizer', methods=['POST'])
@login_required('admin')
def create_organizer():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    department = request.form['department']
    
    # Check if email already exists
    for uid, user in data_store.users.items():
        if user['email'] == email:
            flash('Email already exists', 'error')
            return redirect(url_for('admin.user_management'))
    
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
    
    flash('Organizer created successfully', 'success')
    return redirect(url_for('admin.user_management'))

@admin_bp.route('/toggle-user-status/<user_id>', methods=['POST'])
@login_required('admin')
def toggle_user_status(user_id):
    user = data_store.users.get(user_id)
    if not user or user['role'] == 'admin':
        flash('User not found or unauthorized action', 'error')
        return redirect(url_for('admin.user_management'))
    
    user['is_active'] = not user['is_active']
    status = 'activated' if user['is_active'] else 'deactivated'
    
    flash(f'User {status} successfully', 'success')
    return redirect(url_for('admin.user_management'))

@admin_bp.route('/reports')
@login_required('admin')
def reports():
    # Generate comprehensive reports
    
    # User statistics by role
    user_stats = {
        'students': len([u for u in data_store.users.values() if u['role'] == 'student']),
        'organizers': len([u for u in data_store.users.values() if u['role'] == 'organizer']),
        'total': len([u for u in data_store.users.values() if u['role'] != 'admin'])
    }
    
    # Event statistics
    event_stats = {
        'total': len(data_store.events),
        'approved': len([e for e in data_store.events.values() if e['status'] == 'approved']),
        'pending': len([e for e in data_store.events.values() if e['status'] == 'pending']),
        'rejected': len([e for e in data_store.events.values() if e['status'] == 'rejected'])
    }
    
    # Registration statistics
    reg_stats = {
        'total': len(data_store.registrations),
        'attended': len([r for r in data_store.registrations.values() if r['attended']])
    }
    
    # Popular events (by registration count)
    event_popularity = {}
    for reg in data_store.registrations.values():
        event_id = reg['event_id']
        if event_id in event_popularity:
            event_popularity[event_id] += 1
        else:
            event_popularity[event_id] = 1
    
    popular_events = []
    for event_id, count in sorted(event_popularity.items(), 
                                 key=lambda x: x[1], reverse=True)[:5]:
        event = data_store.events.get(event_id)
        if event:
            popular_events.append({
                'event': event,
                'registrations': count
            })
    
    # Events by category
    category_stats = {}
    for event in data_store.events.values():
        category = event['category']
        if category in category_stats:
            category_stats[category] += 1
        else:
            category_stats[category] = 1
    
    # Monthly registration trends (last 6 months)
    monthly_trends = {}
    six_months_ago = datetime.now() - timedelta(days=180)
    
    for reg in data_store.registrations.values():
        if reg['registered_at'] >= six_months_ago:
            month_key = reg['registered_at'].strftime('%Y-%m')
            if month_key in monthly_trends:
                monthly_trends[month_key] += 1
            else:
                monthly_trends[month_key] = 1
    
    return render_template('admin/reports.html',
                         user_stats=user_stats,
                         event_stats=event_stats,
                         reg_stats=reg_stats,
                         popular_events=popular_events,
                         category_stats=category_stats,
                         monthly_trends=monthly_trends)
