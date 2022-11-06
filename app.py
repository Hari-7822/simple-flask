import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder='template')


base = os.path.abspath(os.path.dirname('database'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class rec(db.Model):


    name = db.Column("user_name", db.String(100), nullable = False)
    phone = db.Column("user_number", db.String(50), nullable = False)
    email = db.Column("user_email", db.String(100), nullable = False)
    userid = db.Column("user_id", db.String(60), primary_key=True, nullable = False)  
    password = db.Column('Password', db.String(100), nullable = False)

    def __ref__(self):
        return f'<Welcome {self.userid} {self.name} >'


@app.route('/register', methods = ('POST', 'GET'))
def reg():

    if request.method == 'POST':
        name_register = request.form['name']
        phone_register = request.form['tele']
        email_register = request.form['email']
        userid_register = request.form['username']
        password_register = request.form['password']

        new = rec(name = name_register, phone = phone_register, email = email_register, userid = userid_register, password = password_register)

        db.session.add(new)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('reg.html.j2')

@app.route('/login', methods = ('GET', 'POST'))
def login():

    if request.method == "POST":
        user = request.form['username']
        passkey = request.form['password']

        chk_name = rec.query.filter_by(userid = user).first()        
        
        if not user or not check_password_hash(user.password, passkey):
            flash('please check your username or password')
            return "welcome" 

        return render_template('login.html.j2')

    return render_template('login.html.j2')



@app.route('/<usr>')
def index(usr):
    return render_template('base.html')

if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader = False)
