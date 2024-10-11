import speech_recognition as sr
from flask import jsonify, request

recognizer = sr.Recognizer()

def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        with sr.AudioFile(file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return jsonify({'transcription': text}), 200

    except sr.UnknownValueError:
        return jsonify({'error': 'Google Speech Recognition could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Could not request results from Google Speech Recognition service; {e}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 501