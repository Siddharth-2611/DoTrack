from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
        else:
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully! You can now login.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))
