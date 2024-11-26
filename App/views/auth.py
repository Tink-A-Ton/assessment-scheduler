from flask import Blueprint, flash, redirect, request, jsonify, render_template, url_for, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_login import logout_user
from werkzeug import Response
from App.controllers.auth import login
from App.controllers.user import is_admin
from App.models.user import User
from App.models.staff import Staff
from App.models.admin import Admin
from App.database import db

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')
    
@auth_views.route('/login', methods=['POST'])
def login_action():
    email: str | None = request.form.get('email')           #To be linked to login button
    password: str | None = request.form.get('password')     #To be linked to login button
    token: str | None = login_user(email, password)
    if token is None:
        flash('Bad email or password given'), 401
        return get_login_page()
    admin: Admin | None = Admin.query.filter_by(email=email).first()
    if admin:
        response: Response = redirect(url_for('admin_views.get_upload_page'))
    else:
        response: Response = redirect(url_for('staff_views.get_calendar_page'))  
    set_access_cookies(response, token) 
    return response           

def login_user(email: str, password: str) -> str | None:
    user: User | None = Admin.query.filter_by(email=email).first() or Staff.query.filter_by(email=email).first()
    print("USER: ", user)
    if user and user.check_password(password):
        token: str = create_access_token(identity=email)
        return token
    return None

@auth_views.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    response: Response = redirect(url_for("auth_views.get_login_page"))
    unset_jwt_cookies(response)
    return response

# @auth_views.route('/identify')
# @jwt_required()
# def identify_view():
#   email = get_jwt_identity()
#   user = User.query.filter_by(email=email).first()
#   if user:
#     return jsonify(user.to_json())
#   return jsonify(message='Invalid user'), 403
