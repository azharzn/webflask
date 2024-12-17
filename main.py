from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/krs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import User, Course

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil, silakan login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login gagal! Username atau password salah.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', username=user.username, email=user.email)
    return redirect(url_for('login'))

@app.route('/krs', methods=['GET', 'POST'])
def krs():
    if 'user_id' in session:
        if request.method == 'POST':
            kode = request.form['kode']
            matkul = request.form['matkul']
            sks = int(request.form['sks'])
            nilai = float(request.form['nilai'])
            course = Course(kode=kode, matkul=matkul, sks=sks, nilai=nilai, user_id=session['user_id'])
            db.session.add(course)
            db.session.commit()
            flash('Mata kuliah berhasil ditambahkan!', 'success')
            return redirect(url_for('krs'))
        courses = Course.query.filter_by(user_id=session['user_id']).all()
        return render_template('krs.html', courses=courses)
    return redirect(url_for('login'))

@app.route('/laporan')
def laporan():
    if 'user_id' in session:
        courses = Course.query.filter_by(user_id=session['user_id']).all()
        total_sks = sum(course.sks for course in courses)
        total_nilai = sum(course.nilai * course.sks for course in courses)
        ipk = total_nilai / total_sks if total_sks > 0 else 0
        status = 'Aktif' if ipk >= 2 else 'Non Aktif'
        course_names = [course.matkul for course in courses]
        course_values = [course.nilai for course in courses]
        return render_template('laporan.html', courses=courses, ipk=ipk, status=status, total_sks=total_sks,
                               course_names=course_names, course_values=course_values)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout!', 'info')
    return redirect(url_for('login'))


