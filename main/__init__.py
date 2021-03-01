from flask import Flask
from flask import g
from flask import jsonify

import os
import yaml
import pymysql

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
database_yaml = "/config/database.yml"

def connect_db():
  with open(basedir + database_yaml) as f:
    doc = yaml.load(f, Loader=yaml.FullLoader)

  return pymysql.connect(
    host= doc["info"]["host"],
    user= doc["info"]["user"],
    passwd= doc["info"]["password"],
    database= doc["info"]["database"]
  )

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route("/")
def index():
  return "Hello World"

@app.route("/emails")
def emails():
  cur = g.db.cursor(pymysql.cursors.DictCursor)
  cur.execute("select * from emails limit 5")
  results = cur.fetchall()

  return_json = { "data": [] }
  for row in results:
    return_json["data"].append({
      "id": row["id"],
      "address": row["address"]
    })

  return jsonify(return_json)