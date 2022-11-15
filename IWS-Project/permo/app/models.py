from hashlib import md5
from time import time
import jwt
from app import app
from datetime import date, datetime
from tokenize import Name
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

request = db.Table('requests',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('status', db.Boolean, index = True),
    db.Column('student_id', db.Integer, db.ForeignKey('user.id'), index=True),
    db.Column('course_id', db.Integer, db.ForeignKey('college_course.id'), index=True)
)   


class User(UserMixin, db.Model):
    firstName = db.Column(db.String(64), index=True)
    lastName = db.Column(db.String(64), index=True)
    id = db.Column(db.Integer, primary_key=True)
    is_professor = db.Column(db.Boolean)
    username = db.Column(db.String(64), index=True, unique=True, )
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('CollegeCourse', backref='professor', lazy='dynamic')
    about_me = db.Column(db.String(140))
    location = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow  )
    verified = db.Column(db.Boolean, default=False)
    verified_on = db.Column(db.DateTime, default=datetime.utcnow)
    requests = db.relationship('User', 
    secondary = request, 
    primaryjoin=(request.c.course_id == id),
    secondaryjoin=(request.c.student_id == id),
    backref=db.backref('requests', lazy='dynamic'), lazy='dynamic')



    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size): ## Gets profile dp from gravatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    

@login.user_loader### Do we need this??
def load_user(id):
    return User.query.get(int(id))


### Work in progress.

### timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) 

class CollegeCourse(db.Model):
    __tablename__ = 'college_course'
    id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.String(20))
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    permission_numbers = db.relationship('permission_numbers', backref='course')
    requests = db.relationship('college_course', 
    secondary = request, 
    primaryjoin=(request.c.course_id == id),
    secondaryjoin=(request.c.student_id == id),
    backref=db.backref('requests', lazy='dynamic'), lazy='dynamic')

    


    def __repr__(self):
        return '<CollegeCourse {}'.format(self.course_name)
    
permission_numbers = db.Table('permission_numbers',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('permission_number', db.Integer),
    db.Column('Assigned', db.Boolean, index=True),
    db.Column('course_name', db.String, db.ForeignKey('college_course.course_name'), index=True),
    db.Column('student_id', db.Integer, db.ForeignKey('user.id'), index=True)
)




