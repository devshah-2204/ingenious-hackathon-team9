from flask import Blueprint, render_template, request, redirect, url_for
from .models import Doctor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from utils import *


docauth = Blueprint('docauth', __name__)


@docauth.route("/doctor/sign-in/", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = (request.form.get('email')).lower()
        password = request.form.get('password')

        doctor_data = load_doctor_data()
        doctor = doctor_data[email]

        if email in doctor_data:
            if check_password_hash(doctor_data[email]['password'], password):
                user = Doctor(
                user_type='doctor',
                email=email,
                password=password,
                first_name=doctor['first_name'],
                last_name=doctor['last_name'],
                mobile=doctor['mobile']
            )
                login_user(user, remember=True)
                return redirect(url_for('docauth.doc_home'))
            else:
                return render_template('login_doctor.html', message="Incorrect password")

        else:
            
            return render_template('login_doctor.html', message="Account with that email does not exist")

    return render_template('login_doctor.html')


@docauth.route("/doctor/sign-up/", methods=['GET', 'POST'])
def signup():
    user_data = load_user_data()
    doctor_data = load_doctor_data()

    if request.method == 'POST':
        first_name = (request.form.get('first_name')).capitalize()
        last_name = (request.form.get('last_name')).capitalize()
        mobile = request.form.get('mobile')
        email = (request.form.get('email')).lower()
        password = request.form.get('password')
        re_password = request.form.get('confirm_password')

        if  email in user_data or email in doctor_data:
            return render_template('signup_doctor.html', message="Email already in use")

        if not check_email(email):
            return render_template('signup_doctor.html', message="Invalid Email")

        if not check_mobile(mobile):
            return render_template('signup_doctor.html', message="Invalid Phone Number")
        
        if password != re_password:
            return render_template('signup_doctor.html', message="Passwords don't match")

        doctor_data[email] = {
            "password": generate_password_hash(password, method="sha256"),
            "first_name": first_name.capitalize(),
            "last_name": last_name.capitalize(),
            "mobile": mobile
        }

        dump_doctor_data(doctor_data)

        doctor = Doctor(
            user_type='doctor',
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
        )

        schedule = create_schedule(email)

        login_user(doctor)
        return redirect(url_for('docauth.details', user=current_user))

    return render_template('signup_doctor.html')


@docauth.route('/doctor/details/', methods=['GET', 'POST'])
def details():
    if request.method == "POST":
        _type = request.form.get('Specialization')
        fee = request.form.get('fee')
        qualification = request.form.get('qualification')
        address = request.form.get('address')
        bio = request.form.get('bio')

        try:
            fee = int(fee)
        except ValueError:
            return render_template('signup_doctor_details.html', user=current_user, message="Invalid Visiting Fee")

        doctor_data = load_doctor_data()
        email = current_user.email

        doctor_data[email]["_type"] = _type
        doctor_data[email]["fee"] = fee
        doctor_data[email]["qualification"] = qualification
        doctor_data[email]["address"] = address
        doctor_data[email]["schedule"] = {}
        doctor_data[email]["bio"] = bio

        dump_doctor_data(doctor_data)

        return redirect(url_for('docauth.doc_home', title="DocAppoint | Home", user=current_user))

    return render_template('signup_doctor_details.html', user=current_user)


@docauth.route("/doctor/home")
def doc_home():
    return render_template("doctor_index.html", title="DocAppoint | Home", user=current_user)

@docauth.route('/doctor/sign-out/')
def logout():
    logout_user()
    return redirect(url_for('docauth.signin'))
