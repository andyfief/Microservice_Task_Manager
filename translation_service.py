from flask import Flask, request, jsonify
from translate import Translator


app = Flask(__name__)
# Special characters in other languages will not display correctly without this set to False
app.json.ensure_ascii = False    # REQUIRED

@app.route('/process_json', methods=['POST'])
def process_json():
    # Receive request with JSON data to be translated
    json_data = request.get_json()

    # Pulls ISO 639 code from "to_language" key to set translation language
    language = json_data["to_language"]
    if not language:
            return jsonify({"error": "Language code is missing"}), 400

    # Set translation language
    translator = Translator(language)

    # Loop through loaded JSON data, retrieve title and task values, translate then replace values
    tasks = json_data.get("tasks", {})
    for index, task in tasks.items():
        try:
            title_translation = translator.translate(task['title'])
            desc_translation = translator.translate(task['description'])
            task['title'] = title_translation
            task['description'] = desc_translation
        except Exception as e:
            print(f"Translation error for task ID {index}: {e}")
    for index, task in tasks.items():
        print(f"Task ID {index}:")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print()
    print("sending tasks to app.py")
    # Return modified JSON data
    return jsonify({"to_language": language, "tasks": tasks})

if __name__ == '__main__':
    app.run(port=5001, debug=True)