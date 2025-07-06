from flask import Blueprint, render_template, session
from app.models import Task
from datetime import datetime

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics')
def statistics():
    if 'user_id' not in session:
        return render_template("statistics.html", labels=[], data=[])

    # Fetch all tasks marked as "Done" for the logged-in user
    done_tasks = Task.query.filter_by(user_id=session['user_id'], status='Done').all()

    labels = []
    data = []

    for task in done_tasks:
        if task.start_time and task.end_time:
            duration = (task.end_time - task.start_time).total_seconds() / 60  # minutes
            if duration > 0:
                labels.append(task.title)
                data.append(round(duration, 2))

    return render_template("statistics.html", labels=labels, data=data)
