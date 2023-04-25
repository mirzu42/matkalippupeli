import json
from flask import Flask
from Projekti.bäkki.database import Database
from flask_cors import CORS

db = Database()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/airport/<iso_country>')
def airport(iso_country):
    sql = f'''SELECT name, latitude_deg, longitude_deg
              FROM airport
              WHERE iso_country=%s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (iso_country,))
    result = cursor.fetchall()
    return json.dumps(result)

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)