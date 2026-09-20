import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('pages/landingpage.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('feed'))
       
    return render_template('login/login.html')

@app.route("/feed")
def feed():
    return render_template('feed/feedinvestidor.html')

@app.route("/register")
def register():
    return render_template('login/register.html')

@app.route('/sobre')
def sobre():
    return render_template('Sobre Nós/sobre.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)