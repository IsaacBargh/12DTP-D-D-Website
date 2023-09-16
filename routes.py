# import flask
from flask import Flask, render_template, abort
import sqlite3


# Create App
app = Flask(__name__)


def sql_connect(query,id=None):
    # takes query, connects DnD.db database and returns all from query
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


@app.route('/')
def home():
    # creates home page and makes title Home
    return render_template("home.html", title="Home")


@app.route('/character')
def character():
    # creates character page and makes title Character Creator
    return render_template("character.html", title="Character Creator")


@app.route('/all_classes')
def all_classes():
    # Creates all_class page using information from the Class table
    group = sql_connect('SELECT * FROM Class')
    return render_template("all_classes.html", title="Class", group=group)


@app.route('/class/<int:id>')
def group(id):
    # Creates class page using information from Class, EquipmentCategory, Feature and spell tables
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Class WHERE id=?', (id,))
    group = cur.fetchone()
    cur.execute('SELECT name FROM EquipmentCategory WHERE id IN(SELECT pid FROM ClassProficiency WHERE cid=?)', (id,))
    proficiency = cur.fetchall()
    cur.execute('SELECT name FROM Feature WHERE id IN(SELECT fid FROM ClassFeature WHERE cid=?)', (id,))
    feature = cur.fetchall()
    cur.execute("SELECT name FROM Spell WHERE id IN(SELECT sid FROM ClassSpell WHERE cid=?)", (id,))
    spell = cur.fetchall()  
    if group != None:
        return render_template('class.html', title=group[1], group=group, proficiency=proficiency, feature=feature, spell=spell)
    else:
        return abort(404)


@app.route('/all_races')
def all_races():
    # Creates All_Races page using information from Race table
    race = sql_connect('SELECT * FROM Race')
    return render_template("all_races.html", title="Race", race=race)


@app.route('/race/<int:id>')
def race(id):
    # Creates Race page using information from Race and Feature table
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Race WHERE id=?', (id,))
    race = cur.fetchone()
    cur.execute('SELECT name FROM Feature WHERE id IN(SELECT fid FROM RaceFeature WHERE rid=?)', (id,))
    feature = cur.fetchall()
    if race != None:
        return render_template("race.html", title=race[1], race=race, feature=feature)
    else:
        return abort(404)


@app.route('/all_equipment')
def all_equipment():
    # Creates All_Equipment page grabs information from Equipment table
    equipment = sql_connect('SELECT * FROM Equipment')
    return render_template("all_equipment.html", title="Equipment", equipment=equipment)


@app.route('/equipment/<int:id>')
def equipment(id):
    # Creates Equipment page grabs information from Equipment
    # and EquipmentCategory table
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Equipment WHERE id=?', (id,))
    equipment = cur.fetchone()
    cur.execute('SELECT name FROM EquipmentCategory WHERE id =(SELECT Category FROM Equipment WHERE id=?)', (id,))
    category = cur.fetchall()
    if equipment != None:
        return render_template("equipment.html", title=equipment[1], equipment=equipment, category=category)
    else:
        return abort(404)


@app.route('/all_schools')
def all_schools():
    # Creates All_Schools page grabs information from School table
    school = sql_connect('SELECT * FROM School')
    return render_template("all_schools.html", title="Spell Schools", school=school)


@app.route('/school/<int:id>')
def school(id):
    # Creates School page grabs information from spell and school table
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Spell WHERE school=?', (id,))
    spell = cur.fetchall()
    cur.execute('SELECT * FROM School WHERE id=?', (id,))
    school = cur.fetchone()
    if school != None:
        return render_template("school.html", title=school[1], school=school, spell=spell)
    else:
        return abort(404)


@app.route('/spell/<int:id>')
def spell(id):
    # Creates Spell page grabs information from spell and school table
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Spell WHERE id=?', (id,))
    spell = cur.fetchone()
    cur.execute('SELECT id FROM School WHERE id= (SELECT school FROM Spell where id=?)', (id,))
    school = cur.fetchone()
    if spell != None:
        return render_template("spell.html", title=spell[1], school=school, spell=spell)
    else:
        return abort(404)


@app.route('/all_features')
def all_features():
    # Create all_feature page using information from Feature table
    features = sql_connect('SELECT * FROM Feature')
    return render_template("all_features.html", title="Features", features=features)


@app.route('/feature/<int:id>')
def feature(id):
    # Create feature page using information from Feature table
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Feature WHERE id=?', (id,))
    features = cur.fetchone()
    if features != None:
        return render_template("feature.html", title=features[1], features=features)
    else:
        return abort(404)

@app.route('/search')
def search():
    # Create Search page using information from all tables
    feature = sql_connect('SELECT * FROM Feature')
    group = sql_connect('SELECT * FROM Class')
    equipment = sql_connect('SELECT * FROM Equipment')
    race = sql_connect('SELECT * FROM Race')
    school = sql_connect('SELECT * FROM School')
    spell = sql_connect('SELECT * FROM Spell')
    return render_template("search.html", title="Search", group=group, feature=feature, equipment=equipment, race=race, school=school, spell=spell)


# Runs app
if __name__ == "__main__":
    app.run(debug=True)
