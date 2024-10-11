from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlite_calls import SQLiteCalls
from transcribe import transcribe_audio
import json

app = Flask(__name__)
CORS(app)

db = SQLiteCalls() 

@app.route('/transcribe', methods=['POST'])
def transcribe():
    return transcribe_audio()

@app.route('/save_question', methods=['POST'])
def add_question():
    data = request.get_json()
    return db.save_question(data)

@app.route('/get_questions', methods=['GET'])
def load_questions():
    questions_df = db.get_questions()
    questions_json = questions_df.to_json(orient='records')
    return jsonify(json.loads(questions_json))

@app.route('/get_user_questions', methods=['GET'])
def load_user_questions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400
    user_questions_df = db.get_user_questions(int(user_id))
    user_questions_json = user_questions_df.to_json(orient='records')
    return jsonify(json.loads(user_questions_json))

@app.route('/save_user', methods=['POST'])
def add_user():
    data = request.get_json()
    return db.save_user(data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return db.login(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)