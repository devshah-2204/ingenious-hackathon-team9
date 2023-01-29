import re
import json
from datetime import datetime

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def check_email(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def check_mobile(mobile):
    mobile = mobile.replace(" ", "")
    
    if len(mobile) != 10:
        return False
    
    try:
        mobile = int(mobile)
    except ValueError:
        return False

    return True


def check_age(age):
    try:
        age = int(age)
    except ValueError:
        return False

    if age > 110:
        return False
    else:
        return True


def load_user_data():
    with open('data/user_data.json', 'r') as f:
        user_data = json.load(f)

    return user_data


def dump_user_data(data):
    try:
        with open('data/user_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    except Exception as e:
        return e

    
def load_doctor_data():
    with open('data/doctor_data.json', 'r') as f:
        doctor_data = json.load(f)

    return doctor_data


def dump_doctor_data(data):
    try:
        with open('data/doctor_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    except Exception as e:
        return e


def load_doctor_professional_data():
    with open('data/doctor_professional_data.json', 'r') as f:
        doctor_professional_data = json.load(f)

    return doctor_professional_data


def dump_doctor_professional_data(data):
    try:
        with open('data/doctor_professional_data.json', 'w') as f:
            json.dump(data, f, indent=4)

        return True
    except Exception as e:
        return e


def create_schedule(doc_email, date=None):
    if date == None:
        date = datetime.now().strftime("%d.%m.%Y")
        
    with open('data/appointments.json', 'r') as f:
        schedule = json.load(f)

    if doc_email not in schedule:
        schedule[doc_email] = {}
    
    if date not in schedule[doc_email]:
        schedule[doc_email][date] = {
            "10.00": "avl",
            "10:30": "avl",
            "11:00": "avl",
            "11:30": "avl",
            "12:00": "avl",
            "12:30": "avl",
            "13:00": "avl",
            "15:30": "avl",
            "16:00": "avl",
            "16:30": "avl",
            "17:00": "avl",
            "17:30": "avl",
        }

    with open('data/appointments.json', 'w') as f:
        json.dump(schedule, f, indent=4)

    return schedule[doc_email]


def load_schedule(doc_email):
    with open('data/appointments.json', 'r') as f:
        schedule = json.load(f)

    if doc_email not in schedule:
        schedule[doc_email] = create_schedule(doctor)

    with open('data/appointments.json', 'w') as f:
        json.dump(schedule, f, indent=4)

    return schedule[doc_email]


def load_entire_schedule():
    with open('data/application.json', 'r') as f:
        schedule = json.load(f)

    return schedule
        