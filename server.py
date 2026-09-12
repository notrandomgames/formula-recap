# server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/standings', methods=['GET'])
def get_standings():
    try:
        res = requests.get('https://api.jolpi.ca/ergast/f1/current/driverstandings.json', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/constructors', methods=['GET'])
def get_constructors():
    try:
        res = requests.get('https://api.jolpi.ca/ergast/f1/current/constructorstandings.json', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/calendar', methods=['GET'])
def get_calendar():
    try:
        res = requests.get('https://api.jolpi.ca/ergast/f1/current.json', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        res = requests.get('https://api.openf1.org/v1/weather?session_key=latest', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
