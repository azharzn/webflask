from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form.get('nama')
        nim = request.form.get('nim')
        jurusan = request.form.get('jurusan')
        email = request.form.get('email')
        kode = request.form.get('kode')
        matkul = request.form.get('matkul')
        sks = int(request.form.get('sks', 0))
        nilai = float(request.form.get('nilai', 0.0))
        ipk = 25/(nilai*sks)

        return render_template('dashboard.html', nama=nama, nim=nim, jurusan=jurusan, email=email, kode=kode,
                               matkul=matkul, sks=sks, nilai=nilai, ipk=ipk)
    return render_template('data.html')


if __name__ == '__main__':
    app.run(debug=True)
