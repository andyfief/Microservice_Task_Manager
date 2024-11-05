from flask import Flask, request, jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback


app = Flask(__name__)

DATA_FILE = 'tasks.json'
EMAIL_ADDRESS = 'enoch25@ethereal.email'
EMAIL_PASSWORD = 'JmT6AtpaqyYbeDwN58'

def load_tasks():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return {}
@app.route('/send_tasks_email', methods=['POST'])
def send_tasks_email():
    try:
        # Load tasks
        data = load_tasks()
        tasks = data.get('tasks', {})
        
        if not tasks:
            return jsonify({'message': 'No tasks to send'}), 400
        
        # Extract recipient and subject from the request
        request_data = request.json
        recipient = request_data.get('recipient')
        subject = request_data.get('subject')
        
        if not recipient or not subject:
            return jsonify({'message': 'Recipient and subject are required'}), 400
        
        # Email setup
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        
        body = "Here is the list of tasks:\n\n"
        for task_id, task in tasks.items():
            title = task.get('title', 'No Title')
            description = task.get('description', 'No Description')
            body += f"ID: {task_id}, Title: {title}, Description: {description}\n"
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP('smtp.ethereal.email', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        
        print(msg.as_string())
        return jsonify({'message': 'Email sent successfully'}), 200
    
    except Exception as e:
        print(f"Error sending email: {e}")
        print(traceback.format_exc())
        return jsonify({'message': f'Failed to send email: {e}'}), 500
    
if __name__ == '__main__':
    app.run(port=5003, debug=True)