from flask import Blueprint, render_template

users_bp = Blueprint('users', __name__)

@users_bp.route('/user/<username>')
def user_profile(username):
    return render_template('user_profile.html', username=username)