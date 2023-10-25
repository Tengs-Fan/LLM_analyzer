import os
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine(os.getenv("DATABASE_URL", "sqlite+pysqlite:///user.db"), echo=True)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

