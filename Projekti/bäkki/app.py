from flask import Flask, render_template, json, request

from database import Database
from flask_cors import CORS

from Lentokenttienhaku import *
from Player import PelaajanHallinta

ph = PelaajanHallinta()

db = Database()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/loc/<loc>')
def currentLoc(loc):
    sql2 = f'''
    SELECT ident, latitude_deg, longitude_deg
    FROM airport
    WHERE ident = %s
    '''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql2, (loc,))
    result = cursor.fetchall()
    json_data = json.dumps(result, default=lambda o: o.__dict__, indent=4)
    return json_data


def fly(loc):
    kentat = []
    nearby = saavutettavatLentokentat(loc)
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