from run import db,app,bcrypt
from sqlalchemy.orm import relationship
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    courses = relationship('Course', backref='user', lazy=True)

# Model Mata Kuliah
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), nullable=False)
    matkul = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    nilai = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
