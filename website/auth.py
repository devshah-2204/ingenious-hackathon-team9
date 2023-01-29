from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from utils import *


auth = Blueprint('auth', __name__)

@auth.route("/sign-in/", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = (request.form.get('email')).lower()
        password = request.form.get('password')

        user_data = load_user_data()

        if email in user_data:
            if check_password_hash(user_data[email]['password'], password):
                user = User(
                user_type='user',
                email=email,
                password=password,
                first_name=user_data[email]['first_name'],
                last_name=user_data[email]['last_name'],
                mobile=user_data[email]['mobile']
            )
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                return render_template('login_user.html', message="Incorrect password")

        else:
            
            return render_template('login_user.html', message="Account with that username does not exist")

    return render_template('login_user.html')


@auth.route("/sign-up/", methods=['GET', 'POST'])
def signup():
    doctor_data = load_doctor_data()
    user_data = load_user_data()

    if request.method == 'POST':
        first_name = (request.form.get('first_name')).capitalize()
        last_name = (request.form.get('last_name')).capitalize()
        mobile = request.form.get('mobile')
        email = (request.form.get('email')).lower()
        password = request.form.get('password')
        re_password = request.form.get('confirm-password')

        if email in doctor_data or email in user_data:
            return render_template('signup_user.html', message="Email already in use")

        if not check_email(email):
            return render_template('signup_user.html', message="Invalid Email")

        if not check_mobile(mobile):
            return render_template('signup_user.html', message="Invalid Phone Number")

        if password != re_password:
            return render_template('signup_user.html', message="Passwords don't match")


        user_data[email] = {
            "password": generate_password_hash(password, method="sha256"),
            "first_name": first_name.capitalize(),
            "last_name": last_name.capitalize(),
            "mobile": mobile
        }

        dump_user_data(user_data)

        user = User(
                user_type='user',
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                mobile=mobile
            )

        login_user(user)
        return redirect(url_for('views.home'))

    return render_template('signup_user.html')


@auth.route("/sign-out/")
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))
