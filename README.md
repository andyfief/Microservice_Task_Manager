# TaskFlow: A Task Management System
 - **An academic project at Oregon State University, CS361 - Software Engineering I**

This project implements a task management system using a microservices architecture with Python's Flask. The system consists of multiple services that handle different aspects of task management, including task storage, email notifications, exporting tasks, and task translation.

## Architecture Overview
The system is composed of the following microservices:

- **Storage Service**: Manages storing and retrieving tasks in JSON format.
- **Email Service**: Sends email notifications containing task lists to specified recipients.
- **Export Service**: Exports tasks to a text file.
- **Search Service**: Allows searching for tasks by ID or keyword.
- **Translation Service** : Translates task titles and descriptions into specified languages.
  
## Technologies Used
- **Flask**: A lightweight WSGI web application framework.
- **JSON**: For data storage and exchange.
- **smtplib**: For sending emails.
- **translate**: A library for translating text.
- **Python**: The programming language used for development.

## Services
- **Storage Service**
  
    Endpoint: `/tasks/search`
  
    Methods: `GET`

    Description: Search for tasks by ID or keyword.
- **Email Service**
  
    Endpoint: `/send_tasks_email`
    
    Methods: `POST`
  
    Description: Sends an email with the current list of tasks.
- **Export Service**
  
  Endpoint: `/export`
  
  Methods: `GET`
  
  Description: Exports the task list to a specified text file.
- **Translation Service**
  
  Endpoint: `/process_json`
  
  Methods: `POST`
  
  Description: Translates task titles and descriptions into the specified language.

## Setup Instructions
  **Clone the Repository:**

```bash
git clone <repository-url>
cd <repository-directory>
```

 **Install Dependencies:**

Ensure you have Python and pip installed. Then, run:

```bash
pip install Flask translate
```

**Run the Services:** Start each service in a separate terminal window:

- Storage Service:
```bash
python task_storage_service.py
```
- Email Service:
```bash
python task_email_service.py
```
- Export Service:
```bash
python task_export_service.py
```
- Search Service:
```bash
python task_search_service.py
```
- Translation Service:
```bash
python task_translation_service.py
```

Each service will be available on different ports:

Storage Service: `http://127.0.0.1:5002`

Email Service: `http://127.0.0.1:5003`

Export Service: `http://127.0.0.1:5004`

Translation Service: `http://127.0.0.1:5001`

## API Documentation

### Storage Service
**Search Tasks**

GET `/tasks/search`

**Query Parameters:**
- `id`: Task ID to search for (optional).

- `query`: Search term to find in task titles or descriptions (optional).
  
**Example Request:**

```bash
GET http://127.0.0.1:5002/tasks/search?id=1
```

### Task Email Service
**Send Tasks Email**

POST `/send_tasks_email`

**Request Body:**

```json
{
    "recipient": "example@example.com",
    "subject": "Task List"
}
```

### Task Export Service
**Export Tasks**

GET `/export`

**Query Parameters:**

`filename`: Name of the export file (optional).

**Example Request:**

```
GET http://127.0.0.1:5004/export?filename=tasks_export.txt
```


### Task Translation Service
**Process JSON:**

POST `/process_json`

**Request Body:***

```json
{
    "to_language": "en",
    "tasks": {
        "1": {
            "title": "walk the cat",
            "description": "take him downtown"
        },
        "2": {
            "title": "my second task",
            "description": "Do this task later"
        }
    }
}
```
