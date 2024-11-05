from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)
DATA_FILE = 'tasks.json'
TRANSLATOR_URL = 'http://127.0.0.1:5001/process_json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
                to_language = data.get('to_language', None)
                tasks = data.get('tasks', {})
                tasks = {int(k): v for k, v in tasks.items()}
                return to_language, tasks
            except json.JSONDecodeError:
                return None, {}
    return None, {}

def save_tasks(to_language, tasks):
    data = {
        'to_language': to_language,
        'tasks': tasks
    }
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def translate_tasks(tasks, to_language):
    if to_language:
        try:
            response = requests.post(TRANSLATOR_URL, json={'to_language': to_language, 'tasks': tasks})
            response.raise_for_status()

            # Print raw response for debugging
            print(f"Raw response text: {response.text}")

            # Attempt to parse JSON response
            try:
                translated_data = response.json()
                return translated_data.get('tasks', {})
            except ValueError as e:
                print(f"JSON decode error: {e}")
                return tasks  # Fallback to the original tasks if parsing fails
        except requests.exceptions.RequestException as e:
            print(f"Translation request failed: {e}")
    return tasks

@app.route('/tasks', methods=['POST'])
def add_task():
    to_language, tasks = load_tasks()
    task_id = max(tasks.keys(), default=0) + 1
    task_data = request.json
    tasks[task_id] = task_data
    save_tasks(to_language, tasks)
    return jsonify({'message': 'Task added', 'task_id': task_id}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    to_language, tasks = load_tasks()
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(to_language, tasks)
        return jsonify({'message': 'Task removed'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    to_language, tasks = load_tasks()
    if task_id in tasks:
        task_data = request.json
        tasks[task_id] = task_data
        save_tasks(to_language, tasks)
        return jsonify({'message': 'Task updated'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/language', methods=['POST'])
def set_language():
    to_language, tasks = load_tasks()
    language = request.json.get('language')
    if language:
        to_language = language
        save_tasks(to_language, tasks)
        return jsonify({'message': 'Language updated'}), 200
    else:
        return jsonify({'message': 'Invalid language'}), 400

@app.route('/tasks', methods=['GET'])
def get_tasks():
    to_language, tasks = load_tasks()
    translated_tasks = translate_tasks(tasks, to_language)
    return jsonify({'tasks': translated_tasks}), 200

if __name__ == '__main__':
    app.run(debug=True)

    