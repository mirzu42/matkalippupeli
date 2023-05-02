from flask import Flask, json, request
from database import Database
from flask_cors import CORS

from Lentokenttienhaku import *
from Player import PelaajanHallinta

ph = PelaajanHallinta()

db = Database()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/loc/<pid>')
def currentLoc(pid):
    sql = f'''
    SELECT location
    FROM player
    WHERE id = %s
    '''
    cursor = db.get_conn().cursor()
    cursor.execute(sql, (pid,))
    location = cursor.fetchone()

    sql2 = f'''
    SELECT ident, latitude_deg, longitude_deg
    FROM airport
    WHERE ident = %s
    '''

    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql2, (location[0],))
    result = cursor.fetchall()

    json_data = json.dumps(result, default=lambda o: o.__dict__, indent=4)
    return json_data


def fly(loc):
    kentat = []

    sql = f'''
    SELECT ident, latitude_deg, longitude_deg
    FROM airport
    WHERE ident = %s
    '''

    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (loc,))
    result = cursor.fetchone()

    nearby = saavutettavatLentokentat(loc)
    kentat.append(result)
    for a in nearby:
        kentat.append(a)
    json_data = json.dumps(kentat, default=lambda o: o.__dict__, indent=4)
    return json_data


@app.route('/flyto')
def flyto():
    args = request.args
    dest = args.get("dest")
    json_data = fly(dest)
    print("*** Called flyto endpoint ***")
    return json_data


@app.route('/airport/<iso_country>')
def airport(iso_country):
    sql = f'''SELECT name, latitude_deg, longitude_deg, ident
              FROM airport
              WHERE iso_country=%s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (iso_country,))
    result = cursor.fetchall()
    return json.dumps(result)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)