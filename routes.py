# import flask
from flask import Flask, render_template, request, redirect, flash
import sqlite3


# Create App
app = Flask(__name__)

def SQL_connect(query):
    conn = sqlite3.connect('DnD.db')   
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


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
    results = SQL_connect('SELECT * FROM Class')
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
    results = SQL_connect('SELECT * FROM Race')
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
    results = SQL_connect('SELECT * FROM Equipment')
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
@app.route('/all_schools')
def all_schools():
    results = SQL_connect('SELECT * FROM School') 
    return render_template("all_schools.html",title="Spell Schools",results=results)


# Create School page grabs information from spell and school table
@app.route('/school/<int:id>')
def school(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Spell WHERE school=?',(id,)) 
    spell = cur.fetchall() 
    cur.execute('SELECT * FROM School WHERE id=?',(id,)) 
    school = cur.fetchone()
    return render_template("school.html",title=school[1],school=school,spell=spell)


    # Create Spell page grabs information from spell and school table
@app.route('/spell/<int:id>')
def spell(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Spell WHERE id=?',(id,)) 
    spell = cur.fetchone() 
    cur.execute('SELECT id FROM School WHERE id= (SELECT school FROM Spell where id=?)',(id,)) 
    school = cur.fetchone()
    return render_template("spell.html",title=spell[1],school=school,spell=spell)

@app.route('/all_features')
def all_features(): 
    results = SQL_connect('SELECT * FROM Feature')
    return render_template("all_features.html",title="Features",results=results)

@app.route('/feature/<int:id>')
def feature(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Feature WHERE id=?',(id,)) 
    results = cur.fetchone() 
    return render_template("feature.html",title=results[1],results=results)


# Create Search page
@app.route('/search')
def search():
    feature = SQL_connect('SELECT * FROM Feature')
    group = SQL_connect('SELECT * FROM Class')
    equipment = SQL_connect('SELECT * FROM Equipment') 
    race = SQL_connect('SELECT * FROM Race') 
    school = SQL_connect('SELECT * FROM School')
    spell = SQL_connect('SELECT * FROM Spell')
    return render_template("search.html", title="Search", group=group, feature=feature, equipment=equipment, race=race, school=school, spell=spell)


# Runs app
if __name__ == "__main__":
    app.run(debug=True)