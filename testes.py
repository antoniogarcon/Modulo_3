import pytest
import requests

# CRUD

BASE_URL = 'http://127.0.0.1:5000'
tasks = []

#Create
def test_create_task():
    new_task_data = {
            "title": "Nova tarefa",
            "description": "Nova tarefa de teste"
        }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200

    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json

    tasks.append(response_json["id"])

# Read
def test_read_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200

    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_read_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']

#UPDATE

def test_update_task():
    if tasks:
        task_id = tasks[0]
        updated_task = {
            "completed": True,
            "description": "Nova descrição",
            "title": "Título atualizado"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_task)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        
        # Recuperando a task alterada e validando com a task
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["completed"] == updated_task["completed"]
        assert response_json["description"] == updated_task["description"]
        assert response_json["title"] == updated_task["title"]
       
#DELETE
def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404