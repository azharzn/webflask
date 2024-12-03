from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'secret'  # Ganti dengan kunci rahasia yang aman
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nama'] = request.form.get('nama')
        session['nim'] = request.form.get('nim')
        session['jurusan'] = request.form.get('jurusan')
        session['email'] = request.form.get('email')
        session['kode'] = request.form.get('kode')
        session['matkul'] = request.form.get('matkul')
        session['sks'] = int(request.form.get('sks', 0))
        session['nilai'] = float(request.form.get('nilai', 0.0))
        session['ipk'] =  (session['nilai'] * session['sks']) / session['sks']
        session['status'] = 'Aktif' if session['ipk'] >= 2 else 'Non Aktif'

        return redirect(url_for('dashboard'))

    return render_template('index.html')
@app.route('/dashboard')
def dashboard():
    if 'nama' in session:
        return render_template('dashboard.html',
                               nama=session['nama'],
                               nim=session['nim'],
                               jurusan=session['jurusan'],
                               email=session['email'])
    return redirect(url_for('index'))
@app.route('/krs')
def krs():
    if 'nama' in session:
        return render_template('krs.html',
                               nama=session['nama'],
                               kode=session['kode'],
                               matkul=session['matkul'],
                               sks=session['sks'])
    return redirect(url_for('index'))

@app.route('/nilai')
def nilai():
    if 'nama' in session:
        return render_template('nilai.html',
                               nama=session['nama'],
                               matkul=session['matkul'],
                               sks=session['sks'],
                               nilai=session['nilai'])
    return redirect(url_for('index'))

@app.route('/laporan')
def laporan():
    if 'nama' in session:
        return render_template('laporan.html',
                               nama=session['nama'],
                               nim=session['nim'],
                               ipk=session['ipk'],
                               sks=session['sks'],
                               status=session['status'])
    return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
