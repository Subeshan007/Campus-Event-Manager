from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import data_store, Team, Submission
from utils import login_required
from datetime import datetime
import uuid

team_bp = Blueprint('team', __name__)

@team_bp.route('/create-team/<event_id>', methods=['GET', 'POST'])
@login_required('student')
def create_team(event_id):
    event = data_store.events.get(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('student.events'))

    if not event.get('is_competition', False):
        flash('This event does not support team registration', 'error')
        return redirect(url_for('student.event_detail', event_id=event_id))

    if request.method == 'POST':
        team_name = request.form['team_name']

        # Check if user is already in a team for this event
        user_teams = [t for t in data_store.teams.values() 
                     if session['user_id'] in t['members'] and t['event_id'] == event_id and t['status'] == 'active']
        if user_teams:
            flash('You are already part of a team for this event', 'error')
            return redirect(url_for('student.event_detail', event_id=event_id))

        # Create new team
        team = Team(team_name, session['user_id'], event_id)
        team_data = {
            'id': team.id,
            'name': team.name,
            'leader_id': team.leader_id,
            'event_id': team.event_id,
            'members': team.members,
            'created_at': team.created_at,
            'status': team.status,
            'team_code': team.team_code
        }

        data_store.teams[team.id] = team_data
        data_store.save_data()

        flash(f'Team "{team_name}" created successfully! Team code: {team.team_code}', 'success')
        return redirect(url_for('team.my_teams'))

    return render_template('student/create_team.html', event=event)

@team_bp.route('/join-team', methods=['GET', 'POST'])
@team_bp.route('/join-team/<event_id>', methods=['GET', 'POST'])
@login_required('student')
def join_team(event_id=None):
    if request.method == 'POST':
        team_code = request.form['team_code'].upper()

        # Find team by code
        team = None
        for t in data_store.teams.values():
            if t['team_code'] == team_code and t['status'] == 'active':
                team = t
                break

        if not team:
            flash('Invalid team code', 'error')
            return render_template('student/join_team.html')

        # Check if user is already in a team for this event
        user_teams = [t for t in data_store.teams.values() 
                     if session['user_id'] in t['members'] and t['event_id'] == team['event_id']]
        if user_teams:
            flash('You are already part of a team for this event', 'error')
            return render_template('student/join_team.html')

        # Check team size limit
        event = data_store.events.get(team['event_id'])
        if event and len(team['members']) >= event.get('team_size_max', 4):
            flash('Team is full', 'error')
            return render_template('student/join_team.html')

        # Add user to team
        team['members'].append(session['user_id'])
        data_store.save_data()

        flash(f'Successfully joined team "{team["name"]}"', 'success')
        return redirect(url_for('team.my_teams'))

    event = None
    if event_id:
        event = data_store.events.get(event_id)
    
    return render_template('student/join_team.html', event=event)

@team_bp.route('/my-teams')
@login_required('student')
def my_teams():
    user_teams = []
    for team in data_store.teams.values():
        if session['user_id'] in team['members']:
            event = data_store.events.get(team['event_id'])
            team_members = []
            for member_id in team['members']:
                member = data_store.users.get(member_id)
                if member:
                    team_members.append(member)

            user_teams.append({
                'team': team,
                'event': event,
                'members': team_members,
                'is_leader': team['leader_id'] == session['user_id']
            })

    return render_template('student/my_teams.html', user_teams=user_teams)

@team_bp.route('/submit/<event_id>', methods=['GET', 'POST'])
@login_required('student')
def submit_project(event_id):
    event = data_store.events.get(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('student.events'))

    # Find user's team for this event
    user_team = None
    for team in data_store.teams.values():
        if session['user_id'] in team['members'] and team['event_id'] == event_id:
            user_team = team
            break

    if not user_team:
        flash('You must be part of a team to submit', 'error')
        return redirect(url_for('student.event_detail', event_id=event_id))

    if request.method == 'POST':
        submission_type = request.form['submission_type']
        content = request.form['content']
        description = request.form['description']

        # Check if team already has a submission
        existing_submission = None
        for sub in data_store.submissions.values():
            if sub['team_id'] == user_team['id'] and sub['event_id'] == event_id:
                existing_submission = sub
                break

        if existing_submission:
            # Update existing submission
            existing_submission['content'] = content
            existing_submission['description'] = description
            existing_submission['submitted_at'] = datetime.now()
            flash('Submission updated successfully!', 'success')
        else:
            # Create new submission
            submission = Submission(user_team['id'], event_id, submission_type)
            submission_data = {
                'id': submission.id,
                'team_id': submission.team_id,
                'event_id': submission.event_id,
                'submission_type': submission.submission_type,
                'content': content,
                'description': description,
                'submitted_at': submission.submitted_at,
                'status': submission.status,
                'score': submission.score,
                'rank': submission.rank
            }
            data_store.submissions[submission.id] = submission_data
            flash('Submission created successfully!', 'success')

        data_store.save_data()
        return redirect(url_for('team.my_teams'))

    # Check for existing submission
    existing_submission = None
    for sub in data_store.submissions.values():
        if sub['team_id'] == user_team['id'] and sub['event_id'] == event_id:
            existing_submission = sub
            break

    return render_template('student/submit_project.html', 
                         event=event, 
                         team=user_team,
                         existing_submission=existing_submission)

@team_bp.route('/leaderboard/<event_id>')
@login_required('student')
def leaderboard(event_id):
    event = data_store.events.get(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('student.events'))

    # Get all submissions for this event
    event_submissions = []
    for submission in data_store.submissions.values():
        if submission['event_id'] == event_id and submission['status'] == 'evaluated':
            team = data_store.teams.get(submission['team_id'])
            if team:
                event_submissions.append({
                    'submission': submission,
                    'team': team
                })

    # Sort by score (descending)
    event_submissions.sort(key=lambda x: x['submission']['score'], reverse=True)

    return render_template('student/leaderboard.html', 
                         event=event, 
                         submissions=event_submissions)