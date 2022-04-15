import json
from flask import Blueprint, redirect, render_template, request, url_for
from . import dbconn
from . import animal

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('login.html', messages = messages)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from animals where email=%s", (email,))
    a = cur.fetchone()
    print(a)
    issetup = False
    if a[6] != 0:
        issetup = True
    ani = animal.Animal(a[2], a[1], a[3], a[4], a[5], issetup)
    if ani.password == password:
        animal.currAnimal = ani
        print(animal.currAnimal)
        if not animal.currAnimal.isSetup:
            return redirect(url_for('main.profileSetup'))
        else:
            return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('auth.login', messages = "Incorrect username or password, please try again"))

@auth.route('/signup')
def signup():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('signup.html', messages = messages)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from animals where email=%s", (email,))
    if len(cur.fetchall())==0:
        a = animal.Animal(email, name, password)
        query, vals = a.insert()
        conn.reconnect()
        cur = conn.cursor()
        cur.execute(query, vals)
        conn.commit()
    else:
        return redirect(url_for('auth.signup', messages = "Email address already exists. Click here to login"))
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    animal.currAnimal = None
    return redirect(url_for('main.index'))