# import flask
from flask import Flask, render_template, request, redirect, flash
import sqlite3


# Create App
app = Flask(__name__)


# Create Home page
@app.route('/')
def home():
    return render_template("home.html", title="Home")


# Create Rules page
@app.route('/rules')
def rules():
    return render_template("rules.html", title="Rules")


# Create All_Classess page grabs information from Class table
@app.route('/all_classes')
def all_classes():
    conn = sqlite3.connect('DnD.db')   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Class')
    results = cur.fetchall()
    return render_template("all_classes.html", title="Class", results=results)


# Create Class page grabs information from Class,EquipmentCategory, 
# Feature and spell table
@app.route('/class/<int:id>')
def group(id):
    conn = sqlite3.connect('DnD.db')   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Class WHERE id=?',(id,))
    group = cur.fetchone()
    cur.execute('SELECT name FROM EquipmentCategory WHERE id IN(SELECT pid FROM ClassProficiency WHERE cid=?)',(id,))
    proficiency = cur.fetchall()
    cur.execute('SELECT name FROM Feature WHERE id IN(SELECT fid FROM ClassFeature WHERE cid=?)',(id,))
    feature = cur.fetchall() 
    cur.execute("SELECT name FROM Spell WHERE id IN(SELECT sid FROM ClassSpell WHERE cid=?)",(id,))
    spell= cur.fetchall() 
    return render_template('class.html',title=group[1],group=group, proficiency=proficiency, feature=feature, spell=spell)


# Create All_Races page grabs information from Race table
@app.route('/all_races')
def all_races():
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Race')
    results = cur.fetchall()
    return render_template("all_races.html",title="Race",results=results)


# Create Race page grabs information from Race and Feature table
@app.route('/race/<int:id>') 
def race(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Race WHERE id=?',(id,)) 
    race = cur.fetchone() 
    cur.execute('SELECT name FROM Feature WHERE id IN(SELECT fid FROM RaceFeature WHERE rid=?)',(id,))
    feature = cur.fetchall() 
    return render_template("race.html",title=race[1],race=race, feature=feature)


# Create All_Equipment page grabs information from Equipment table
@app.route('/all_equipment')
def all_equipment():
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Equipment') 
    results = cur.fetchall() 
    return render_template("all_equipment.html",title="Equipment",results=results)


# Create Equipment page grabs information from Equipment and EquipmentCategory table
@app.route('/equipment/<int:id>')
def equipment(id):
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Equipment WHERE id=?',(id,)) 
    results = cur.fetchone()
    cur.execute('SELECT name FROM EquipmentCategory WHERE id =(SELECT Category FROM Equipment WHERE id=?)',(id,))
    category= cur.fetchall() 
    return render_template("equipment.html",title=results[1],results=results, category=category)


# Create All_Schools page grabs information from School table
@app.route('/schools')
def schools():
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM School') 
    results = cur.fetchall() 
    return render_template("schools.html",title="Spells",results=results)


# Create Spell page grabs information from spell and school table
@app.route('/spells/<int:id>')
def spells(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Spell WHERE school=?',(id,)) 
    spell = cur.fetchall() 
    cur.execute('SELECT * FROM School WHERE id=?',(id,)) 
    school = cur.fetchone()
    return render_template("spells.html",title=school[1],school=school,spell=spell)


# Runs app
if __name__ == "__main__":
    app.run(debug=True)