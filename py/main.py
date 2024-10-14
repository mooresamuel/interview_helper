import os
import json

import pandas as pd
import numpy as np

from dotenv import load_dotenv
from sqlite_calls import SQLiteCalls
from anthropic_calls import AnthropicCalls
from sklearn.metrics.pairwise import cosine_similarity


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

db = SQLiteCalls()

# @app.route('/generate_questions', methods=['POST'])
# def generate_questions():
#     data = request.get_json()
#     return gen_questions(data)

# def gen_questions(data):
#     job_title = data['job_title']
#     experience = data['experience']

@app.route('/test')
def test():
    return "Test successful!"


# @app.route('/transcribe', methods=['POST'])
# def transcribe():
#     return transcribe_audio()

@app.route('/move_into_user_questions', methods=['POST'])
def move_into_user_questions():
    data = request.get_json()
    return db.move_into_user_questions(data)


@app.route('/move_out_of_user_questions', methods=['POST'])
def move_out_of_user_questions():
    data = request.get_json()
    return db.move_out_of_user_questions(data)

@app.route('/save_question', methods=['POST'])
def save_question():
    data = request.get_json()
    return db.save_question(data)

@app.route('/add_user_question', methods=['POST'])
def add_user_question():
    data = request.get_json()
    return db.save_user_question(data)

@app.route('/get_questions', methods=['GET'])
def load_questions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400
    questions_df = db.get_questions(int(user_id))
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
    app.run(host='0.0.0.0', port=8001, debug=True)