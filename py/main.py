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

@app.route('/test')
def test():
    return "Test successful!"


# @app.route('/transcribe', methods=['POST'])
# def transcribe():
#     return transcribe_audio()

@app.route('/unassign_question', methods=['POST'])
def unassign_question():
    data = request.get_json()
    return db.unassign_question(data)

@app.route('/assign_question', methods=['POST'])
def assign_question():
    data = request.get_json()
    return db.assign_question(data)

@app.route('/load_questions', methods=['GET'])
def load_questions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400
    questions_df = db.load_questions(user_id)
    questions_json = questions_df.to_json(orient='records')
    return jsonify(json.loads(questions_json))

@app.route('/save_question', methods=['POST'])
def save_question():
    data = request.get_json()
    return db.save_question(data)

# @app.route('/add_user_question', methods=['POST'])
# def add_user_question():
#     data = request.get_json()
#     return db.save_user_question(data)

# @app.route('/get_questions', methods=['GET'])
# def load_questions():
#     user_id = request.args.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'Missing user_id parameter'}), 400
#     questions_df = db.get_questions(int(user_id))
#     questions_json = questions_df.to_json(orient='records')
#     return jsonify(json.loads(questions_json))

@app.route('/get_user_questions', methods=['GET'])
def load_user_questions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400
    user_questions_df = db.get_user_questions(int(user_id))
    user_questions_json = user_questions_df.to_json(orient='records')
    return jsonify(json.loads(user_questions_json))

#------------------------NEW-------------------------
# @app.route('/get_generated_questions', methods=['GET'])
# def load_generated_questions():
#     user_id = request.args.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'Missing user_id parameter'}), 400
#     user_questions_df = db.get_generated_questions(int(user_id))
#     user_questions_json = user_questions_df.to_json(orient='records')
#     return jsonify(json.loads(user_questions_json))
# #------------------------END-------------------------
@app.route('/save_user', methods=['POST'])
def add_user():
    data = request.get_json()
    return db.save_user(data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return db.login(data)

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    result = db.generate_questions(data)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)