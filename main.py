import os
from flask import Blueprint, abort, redirect, request, url_for
from flask import render_template
from __init__ import dbconn
from animal import animal

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    print(animal.currAnimal)
    if not animal.currAnimal:
        return redirect(url_for('auth.login'))

    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from animals where email=%s", (animal.currAnimal.email,))
    return redirect(url_for('main.route_animal', animalid=cur.fetchone()[0]))

@main.route("/profileSetup")
def profileSetup():
    return render_template('profileSetup.html', currani = animal.currAnimal)

@main.route("/profileSetup", methods=['POST'])
def profileSetup_post():
    print("here")
    UPLOAD_FOLDER = 'static/'
    print(request.files['file'])
    file = request.files['file']
    species = request.form.get('species')
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    animal.currAnimal.species = species
    animal.currAnimal.image = filename

    query, vals = animal.currAnimal.profileSetup()

    conn = dbconn()
    cur = conn.cursor()
    cur.execute(query, vals)
    conn.commit()
    return redirect(url_for('main.profile'))
         

@main.route('/<int:animalid>')
def route_animal(animalid):
    if not animal.currAnimal:
        return redirect(url_for('auth.login'))
        
    ani = list(get_animal(animalid))
    print(ani)
    if not ani[5]:
        ani[5] = "notfound"
    return render_template('animal.html', ani=ani)


def get_animal(animalid):
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from animals where id=%s", (animalid,))
    animal = cur.fetchone()
    conn.close()
    if animal is None:
        abort(404)
    return animal
