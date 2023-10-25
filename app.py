from flask import Flask
from flask_login import LoginManager

from dotenv import load_dotenv
load_dotenv()
# from user import User  # Import the User class from user.py

def create_app():
    app = Flask(__name__)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    # login_manager.login_view = 'login' # type: ignore
    login_manager.login_message = u"Welcome to the WRDS150B database"

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.run(debug=True)


if __name__ == '__main__':
    create_app()
