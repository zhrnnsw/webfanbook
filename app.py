import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/homework', methods=['POST'])
def homework_post():
    db.fanmessages.insert_one({
        'name': request.form['name_give'],
        'comment': request.form['comment_give']
    })
    return jsonify({
        'msg': 'POST messages!'
    })

@app.route('/homework')
def homework_get():
    return jsonify({
        'messages': list(db.fanmessages.find({}, {'_id': False}))
    })
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)