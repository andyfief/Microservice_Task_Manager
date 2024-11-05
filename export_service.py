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
                return tasks
            except json.JSONDecodeError:
                return {}
    return {}

@app.route('/export', methods=['GET'])
def export_tasks():
    filename = request.args.get('filename', 'tasks_export.txt')  # Default to tasks_export.txt if not provided
    tasks = load_tasks()
    if not tasks:
        return jsonify({'Export message': 'No tasks found'}), 404

    # Sort tasks alphabetically by title
    sorted_tasks = sorted(tasks.values(), key=lambda x: x.get('title', ''))
    print(f"Sorted tasks: {sorted_tasks}")
    try:
        with open(filename, 'w') as file:
            for task in sorted_tasks:
                title = task.get('title', 'No Title')
                description = task.get('description', 'No Description')
                file.write(f"{title}\n\t{description}\n\n")  # Indent description with a tab
    except IOError as e:
        return jsonify({'Export message': f'Error writing to file: {e}'}), 500

    return jsonify({'Export message': f'Success! Tasks exported to {filename}'}), 200

if __name__ == '__main__':
    app.run(port=5004, debug=True)