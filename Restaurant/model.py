from datetime import datetime
from Restaurant import db, login_manager
from flask_login import  UserMixin
import json
@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(int(user_id))
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
class reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    phone=db.Column(db.Integer)
    seats=db.Column(db.Integer)
    dateandtime=db.Column(db.DateTime)


class JsonEcodedcart(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'  # Return an empty JSON array if the value is None
        else:
            return json.dumps(value)  # Serialize the list of dictionaries to a JSON string

    def process_result_value(self, value, dialect):
        if value is None:
            return []  # Return an empty list if the value is None
        else:
            return json.loads(value)
class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedcart)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice



# from app import app, User
# >>>
# >>> # Create the Flask application context
# >>> with app.app_context():
# ...     # Now you can safely use Flask-SQLAlchemy within this context
# ...     users = User.query.all()
# ...     for user in users:
# ...         print(user.username, user.email)
# ... 