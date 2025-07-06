from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    title = request.form['title']
    task = Task(title=title, status='Pending', user_id=session['user_id'], start_time=datetime.now())
    db.session.add(task)
    db.session.commit()
    flash('Task added', 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task.user_id != session['user_id']:
        flash('Access denied', 'danger')
        return redirect(url_for('tasks.view_tasks'))

    if task.status == 'Pending':
        task.status = 'Working'
        task.start_time = datetime.now()
    elif task.status == 'Working':
        task.status = 'Done'
        task.end_time = datetime.now()
    else:
        task.status = 'Pending'
        task.start_time = None
        task.end_time = None

    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=["POST"])
def clear_tasks():
    Task.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash('All tasks cleared', 'info')
    return redirect(url_for('tasks.view_tasks'))
