import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('pages/landingpage.html')

@app.route("/login")
def login():
    return render_template('login/login.html')

@app.route("/select-role")
def select_role():
    return render_template('login/register/select_role.html')

# Rotas de cadastro
@app.route("/register/student")
def register_student():
    return render_template('login/register/register_student.html')

@app.route("/register/company")
def register_company():
    return render_template('login/register/register_company.html')

@app.route("/register/visitor")
def register_visitor():
    return render_template('login/register/register_visitor.html')

@app.route('/sobre')
def sobre():
    return render_template('Sobre Nós/sobre.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

def main():
   app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 10000)))