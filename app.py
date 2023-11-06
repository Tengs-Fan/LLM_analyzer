import os
from flask import Flask
from flask_login import LoginManager

from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'my-secret-key')  # Provide a fallback default if not set in environment

    # Session settings
    from datetime import timedelta
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=1800)  # 30 minutes
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # type: ignore
    login_manager.login_message = u"Welcome to the WRDS150B database"

    from user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Error handlers
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('Server Error: %s', (error))
        return "500 error"
    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.error('Unhandled Exception: %s', (e))
        return 'Unhandled Exception', 500

    # Logging 
    import logging
    from logging.handlers import RotatingFileHandler
    logging.basicConfig(filename='app.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # setup_logging(app)
    return app

if __name__ == '__main__':
    app = create_app()
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8088, debug=True)

def setup_logging(app):
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/wrds.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('WRDS150B startup')

