import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')


base = os.path.abspath(os.path.dirname('database'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class rec(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)  
    name = db.Column("name", db.String(100), nullable = False)
    role = db.Column("role", db.String(80), nullable = False)

    def __ref__(self):
        return f'<Welcome {self.role} {self.name} >'


@app.route('/register', methods = ('POST', 'GET'))
def reg():

    if request.method == 'POST':
        id1 = request.form['id']
        name1 = request.form['name']
        role1 = request.form['role']

        st = rec(id = id1, name = name1, role = role1)

        db.session.add(st)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('reg.html.j2')

@app.route('/login', methods = ('GET', 'POST'))
def login():

    if request.method == "POST":
        user = request.form.get['username']
        roles = request.form.get['role']

        chk_name = user.query.filter(name = user).first()
        chk_role = user.query.filter(role = roles).first()
        
        

        return render_template('login.html.j2')

    return render_template('base.html')



@app.route('/<usr>')
def index(usr):
    return render_template('base.html', usr = name)

if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader = False)
