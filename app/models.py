from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model): #Database entry of a user
    id=db.Column(db.Integer, primary_key=True) #SQLAlchemy requires a primary key
    username=db.Column(db.String(64), index=True, unique=True) #Index makes searches quicker
    password=db.Column(db.String(128))

    def set_pass(self, password): #Hashes the current password
        self.password = generate_password_hash(password)
    
    def check_pass(self, password): #checks the hashed password against the user input
        return check_password_hash(self.password, password)

    def printUser(self):
        return str(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
