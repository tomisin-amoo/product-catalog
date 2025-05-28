from flask_login import UserMixin
from . import db

# --- User model stored in PostgreSQL ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Will store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'


# --- Product model (same as before, keep this) ---
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.Text)