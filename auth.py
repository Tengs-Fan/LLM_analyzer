from user import User
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from logging import getLogger
 
auth = Blueprint('auth', __name__)
logger = getLogger(__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.get(user_id)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            logger.info(f"User {user_id} logged in successfully.")
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.')
            logger.warning(f"Failed login attempt for user {user_id}.")
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logger.info(f"User {current_user} logged out.")
    logout_user()
    return redirect(url_for('main.index'))

