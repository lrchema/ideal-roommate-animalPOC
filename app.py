from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

hostname = 'localhost'
username = 'root'
password = 'password'
database = 'testdb'


def dbconn():
    return mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)


@app.route('/')
def index():
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from animals")
    animals = cur.fetchall()
    conn.close()
    return render_template('index.html', animals=animals)


@app.route('/<int:animalid>')
def animal(animalid):
    animal = get_animal(animalid)
    return render_template('animal.html', animal=animal)


def get_animal(animalid):
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    print(animalid)
    cur.execute("select * from animals where id=%s", (animalid,))
    animal = cur.fetchone()
    conn.close()
    if animal is None:
        abort(404)
    return animal
