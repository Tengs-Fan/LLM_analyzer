import os
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine(os.getenv("DATABASE_URL", "sqlite+pysqlite:///user.db"), echo=True)

creation_users = text('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    password_hash TEXT
);
''')
with engine.connect() as conn:
    result = conn.execute(creation_users)

class User:
    def __init__(self, id=None, password=None, password_hash=None):
        self.id = id
        if password:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = password_hash
        self._is_authenticated = False
        self._is_active = True
        self.is_anonymous = False

    # Flask-Login compatibility
    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self._is_active
 
    @property
    def is_authenticated(self):
        return self._is_authenticated   

    # Database interactions
    @classmethod
    def get(cls, user_id):
        sql = text("SELECT id, password_hash FROM users WHERE id = :user_id")
        with engine.connect() as conn:
            result = conn.execute(sql, {"user_id": user_id}).fetchone()
            if result:
                return cls(id=result[0], password_hash=result[1])
    
    def save(self):
        sql = text(
            """
            INSERT INTO users (id, password_hash) VALUES (:id, :password_hash)
            ON CONFLICT(id) DO UPDATE SET password_hash = :password_hash
            """
        )
        with engine.connect() as conn:
            conn.execute(sql, { "id" : self.id, "password_hash" : self.password_hash})
