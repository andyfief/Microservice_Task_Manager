from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
                tasks = data.get('tasks', {})
                tasks = {int(k): v for k, v in tasks.items()}
                return tasks
            except json.JSONDecodeError:
                return {}
    return {}

@app.route('/tasks/search', methods=['GET'])
def search_tasks():
    tasks = load_tasks()
    task_id = request.args.get('id')
    query = request.args.get('query')
    
    if task_id:
        task_id = int(task_id)
        result = {task_id: tasks.get(task_id, None)}
        return jsonify({'tasks': result}), 200 if task_id in tasks else 404
    
    if query:
        results = {k: v for k, v in tasks.items() if query.lower() in v['title'].lower() or query.lower() in v['description'].lower()}
        return jsonify({'tasks': results}), 200
    
    return jsonify({'tasks': {}}), 400  # Return an empty tasks object if no search criteria

if __name__ == '__main__':
    app.run(port=5002, debug=True)