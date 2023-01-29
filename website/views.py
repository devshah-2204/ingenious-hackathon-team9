from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from utils import *


views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        _type = request.form.get('Specialization')
        date = request.form.get('date')

        date = date.replace("-", " ")
        date = date.split()
        date = f"{date[2]}.{date[1]}.{date[0]}"
    
        doctor_data = load_doctor_data()
        doctors = {}


        for email in doctor_data:
            if doctor_data[email]['_type'] == _type:
                schedule = create_schedule(email, date)
                for time_slot in schedule[date]:
                    if schedule[date][time_slot] == "avl":
                        doctors[email] = doctor_data[email]

        if doctors == {}:
            avl = False
        else:
            avl = True

        return render_template('available_doctors.html', user=current_user, doctors=doctors, avl=avl)

    return render_template('index.html', user=current_user, title="DocAppoint | Home")


@views.route("/search/", methods=['GET', 'POST'])
def search():
    return render_template('available_doctors.html', user=current_user)


@views.route('/appointment/', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        email = request.form.get('email-post')

    doctor_data = load_doctor_data()

    return render_template('doctor_profile.html', user=current_user, doctor=doctor_data[email])