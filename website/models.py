from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_type, email, first_name, last_name, password, mobile):
        self.user_type = "user"
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.mobile = mobile
        self.id = email


class Doctor(UserMixin):
    def __init__(self, user_type, email, first_name, last_name, password, mobile):
        self.user_type = "doctor"
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.mobile = mobile
        self.id = email
        


class Details(Doctor):
    def __init__(self, _type, fee, qualification, address, bio):
        self._type = _type
        self.fee = fee
        self.qualification = qualification
        self.address = address
        self.bio = bio


class Appointment():
    def __init__(self, user: User, doctor: Doctor, date, time_slot):
        self.user = user
        self.doctor = doctor
        self.date = date
        self.time_slot = time_slot
