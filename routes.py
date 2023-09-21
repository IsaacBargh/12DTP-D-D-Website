# import necessary commands from flask and sqlite3
from flask import Flask, render_template, abort
import sqlite3


# Creates App
app = Flask(__name__)


def sql_connect(query, id=None, fetchall=True):
    # Connects to DnD.db
    conn = sqlite3.connect('DnD.db')
    cur = conn.cursor()
    # checks if given new id
    if id is not None:
        # executes given query for given id
        cur.execute(query, id)
    else:
        # executes given query
        cur.execute(query)
    # checks if fetchone
    if fetchall is False:
        # returns one result
        return cur.fetchone()
    else:
        # returns all results
        return cur.fetchall()


@app.route('/')
def home():
    # renders home.html and makes title Home
    return render_template("home.html", title="Home")


@app.route('/character')
def character():
    # renders character.html and makes title Character Creator
    return render_template("character.html", title="Character Creator")


@app.route('/all_classes')
def all_classes():
    # runs sql_connect function where query equals 'SELECT * FROM Class'
    group = sql_connect('SELECT * FROM Class')
    # renders all_class.html using information from the Class table so that I
    # only grab the information that will be used
    return render_template("all_classes.html", title="Class", group=group)


@app.route('/class/<int:id>')
def group(id):
    # only grabs necessary information from database for choosen class
    # selects one row from the Class table that matches given id
    group = sql_connect('SELECT * FROM Class WHERE id=?', (id,), False)
    # selects the name of all EquipmentCategories that have an id matched with
    # the given class id in the ClassProficiency table
    proficiency = sql_connect('SELECT name FROM EquipmentCategory WHERE id IN'
                              '(SELECT pid FROM ClassProficiency WHERE cid=?)',
                              (id,))
    # selects the name of all Features that have an id matched with
    # the given class id in the ClassFeature table
    feature = sql_connect('SELECT name FROM Feature WHERE id IN'
                          '(SELECT fid FROM ClassFeature WHERE cid=?)', (id,))
    # selects the name of all spells that have an id matched with
    # the given class id in the ClassSpell table
    spell = sql_connect('SELECT name FROM Spell WHERE id IN'
                        '(SELECT sid FROM ClassSpell WHERE cid=?)', (id,))
    # checks information was received from class table
    if group:
        # renders class.html with variables group, proficiency, feature and
        # spell to store information pulled from database above and make the
        # title equal to the name of the choosen class
        return render_template('class.html', title=group[1], group=group,
                               proficiency=proficiency, feature=feature,
                               spell=spell)
    else:
        # returns 404 error if no information is grabbed from class table
        return abort(404)


@app.route('/all_races')
def all_races():
    # renders all_race.html using information from the Race table so that I
    # only grab the information that will be used
    race = sql_connect('SELECT * FROM Race')
    return render_template("all_races.html", title="Race", race=race)


@app.route('/race/<int:id>')
def race(id):
    # only grabs necessary information from database for choosen race
    race = sql_connect('SELECT * FROM Race WHERE id=?', (id,), False)
    # selects the name of all features that have an id matched with
    # the given race id in the RaceFeature table
    feature = sql_connect('SELECT name FROM Feature WHERE id IN'
                          '(SELECT fid FROM RaceFeature WHERE rid=?)', (id,))
    if race:
        # renders race.html and make the title equal to the name of the
        # choosen race
        return render_template("race.html", title=race[1], race=race,
                               feature=feature)
    else:
        return abort(404)


@app.route('/all_equipment')
def all_equipment():
    # renders all_equipment.html using information from the Equipment table so
    # that I only grab the information that will be used
    equipment = sql_connect('SELECT * FROM Equipment')
    return render_template("all_equipment.html", title="Equipment",
                           equipment=equipment)


@app.route('/equipment/<int:id>')
def equipment(id):
    # only grabs necessary information from database for choosen equipment
    equipment = sql_connect('SELECT * FROM Equipment WHERE id=?', (id,), False)
    # selects the name of the equipmentcategory that has an id matched with
    # the Category from the choosen equipment
    category = sql_connect('SELECT name FROM EquipmentCategory WHERE id ='
                           '(SELECT Category FROM Equipment WHERE id=?)',
                           (id,))
    if equipment:
        # renders equipment.html and make the title equal to the name of the
        # choosen equipment
        return render_template("equipment.html", title=equipment[1],
                               equipment=equipment, category=category)
    else:
        return abort(404)


@app.route('/all_schools')
def all_schools():
    # renders all_school.html using information from the school table so
    # that I only grab the information that will be used
    school = sql_connect('SELECT * FROM School')
    return render_template("all_schools.html", title="Spell Schools",
                           school=school)


@app.route('/school/<int:id>')
def school(id):
    # only grabs necessary information from database for choosen school
    spell = sql_connect('SELECT * FROM Spell WHERE school=?', (id,))
    school = sql_connect('SELECT * FROM School WHERE id=?', (id,), False)
    if school:
        # renders school.html and make the title equal to the name of the
        # choosen school
        return render_template("school.html", title=school[1], school=school,
                               spell=spell)
    else:
        return abort(404)


@app.route('/spell/<int:id>')
def spell(id):
    # only grabs necessary information from database for choosen spell
    spell = sql_connect('SELECT * FROM Spell WHERE id=?', (id,), False)
    # selects the name of the school that has an id matched with
    # the school from the choosen spell
    school = sql_connect('SELECT name FROM School WHERE id='
                         '(SELECT school FROM Spell where id=?)', (id,), False)
    if spell:
        # renders spell.html and make the title equal to the name of the
        # choosen spell
        return render_template("spell.html", title=spell[1], school=school,
                               spell=spell)
    else:
        return abort(404)


@app.route('/all_features')
def all_features():
    # renders all_feature.html using information from the Feature table so
    # that I only grab the information that will be used
    features = sql_connect('SELECT * FROM Feature')
    return render_template("all_features.html", title="Features",
                           features=features)


@app.route('/feature/<int:id>')
def feature(id):
    # only grabs necessary information from database for choosen feature
    # renders feature.html using information from Feature table
    # conn = sqlite3.connect('DnD.db')
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM Feature WHERE id=?', (id,))
    # features = cur.fetchone()
    features = sql_connect('SELECT * FROM Feature WHERE id=?', (id,), False)
    if features:
        # renders feature.html and make the title equal to the name of the
        # choosen feature
        return render_template("feature.html", title=features[1],
                               features=features)
    else:
        return abort(404)


@app.route('/search')
def search():
    # renders search.html using id and name from all tables so only the
    # information needed to create links to each information page is
    feature = sql_connect('SELECT id, name FROM Feature')
    group = sql_connect('SELECT id, name FROM Class')
    equipment = sql_connect('SELECT id, name FROM Equipment')
    race = sql_connect('SELECT id, name FROM Race')
    school = sql_connect('SELECT id, name FROM School')
    spell = sql_connect('SELECT id, name FROM Spell')
    return render_template("search.html", title="Search", group=group,
                           feature=feature, equipment=equipment, race=race,
                           school=school, spell=spell)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Error 404"), 404


# Runs app
if __name__ == "__main__":
    app.run(debug=True)
