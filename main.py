from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('dashboard.html')

@app.route('/masuk', methods = ['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        return render_template('dashboard.html', username=username)
    return render_template('login.html')

@app.route('/detail')
def Detail():
    img_name = request.args.get('img_name', 'default_img')
    return render_template('detail.html', img_name=img_name)

if __name__ == '__main__':
    app.run(debug=True)
