from flask import Flask
from flask_login import LoginManager, logout_user
from utils import *

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config['SECRET_KEY'] = 'hackathon1'

    from .views import views
    from .auth import auth
    from .docauth import docauth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(docauth, url_prefix='/')
    
    from .models import User, Doctor

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(email):
        user_data = load_user_data()
        doctor_data = load_doctor_data()

        if email in user_data:
            try:
                user = user_data[email]

                return User(
                    user_type='user',
                    email=email,
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    password=user['password'],
                    mobile=user['mobile']
                )

            except:
                pass
        
        else:
            try:
                user = doctor_data[email]

                return Doctor(
                    user_type='doctor',
                    email=email,
                    password=user['password'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    mobile=user['mobile']
                )
            except:
                pass

    return app