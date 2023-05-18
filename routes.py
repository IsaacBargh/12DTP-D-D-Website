from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",title="Home")

@app.route('/rules')
def rules():
    return render_template("rules.html",title="Rules")

@app.route('/all_classes')
def all_classes():
    conn = sqlite3.connect('DnD.db')   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Class')
    results = cur.fetchall()
    return render_template("all_classes.html",title="Classes",results=results)

@app.route('/class/<int:id>')
def group(id):
    conn = sqlite3.connect('DnD.db')   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Class WHERE id=?',(id,))
    group = cur.fetchone()
    cur.execute('SELECT name FROM EquipmentCategory WHERE id IN(SELECT pid FROM ClassProficiency WHERE cid=?)',(id,))
    proficiency= cur.fetchall()
    cur.execute('SELECT name FROM Feature WHERE id IN(SELECT fid FROM ClassFeature WHERE cid=?)',(id,))
    feature = cur.fetchall() 
    cur.execute("SELECT name FROM Spell WHERE id IN(SELECT sid FROM ClassSpell WHERE cid=?)",(id,))
    spell= cur.fetchall() 
    return render_template('class.html',title="Class",group=group, proficiency=proficiency, feature=feature, spell=spell)

@app.route('/all_races')
def all_races():
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Race')
    results = cur.fetchall()
    return render_template("all_races.html",title="Races",results=results)

@app.route('/race/<int:id>') 
def race(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Race WHERE id=?',(id,)) 
    race = cur.fetchone() 
    cur.execute('SELECT name FROM Feature WHERE id IN(SELECT fid FROM RaceFeature WHERE rid=?)',(id,))
    feature = cur.fetchall() 
    return render_template("race.html",title="Race",race=race, feature=feature)

@app.route('/all_equipment')
def all_equipment():
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Equipment') 
    results = cur.fetchall() 
    return render_template("all_equipment.html",title="Equipment-List",results=results)


@app.route('/equipment/<int:id>')
def equipment(id):
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Equipment WHERE id=?',(id,)) 
    results = cur.fetchone()
    cur.execute('SELECT name FROM EquipmentCategory WHERE id =(SELECT Category FROM Equipment WHERE id=?)',(id,))
    category= cur.fetchall() 
    return render_template("equipment.html",title="Equipment",results=results, category=category)

@app.route('/schools')
def schools():
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM School') 
    results = cur.fetchall() 
    return render_template("schools.html",title="Spell-Schools",results=results)

@app.route('/spells/<int:id>')
def spells(id): 
    conn = sqlite3.connect('DnD.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM Spell WHERE school=?',(id,)) 
    spell = cur.fetchall() 
    cur.execute('SELECT * FROM School WHERE id=?',(id,)) 
    school = cur.fetchone()
    return render_template("spells.html",title="Spells",school=school,spell=spell)


if __name__ == "__main__":
    app.run(debug=True)