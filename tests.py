#python -m unittest tests.py
# and same dir

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from mainMySQL import app
from auth_test import verify_token


class TestSample(unittest.TestCase):  
    def setUp(self):
        # Set up the TestClient and mock token
        self.client = TestClient(app)
        # Update every 30 minutes
        self.mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCZWhhbiIsImV4cCI6MTczMDY3MzMyMH0.TkGOzHKqdA2z3CJmMfsLv4xPfysIHN490ye71K7n8Bg"  # This is your mocked token value
    
    #Test 200 Response Code mit auth
    @patch("mainMySQL.verify_token")
    def test_get_tasks(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        response = self.client.get("/tasks/", headers=headers)
        self.assertEqual(response.status_code, 200)
        
    #Test 401 ohne Auth abfrage     
    def test_get_tasks_no_auth(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 401)
        
    #Test get gibt eine Liste zurück    
    @patch("mainMySQL.verify_token")
    def test_get_tasks_list(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        response = self.client.get("/tasks/", headers=headers)
        self.assertIsInstance(response.json(), list)
        
    #Test nur den richtigen User seine Tasks sichtbar
    @patch("mainMySQL.verify_token")
    def test_get_tasks_list_user(self, mock_verify_token):
        userid = verify_token(token=self.mock_token)
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        response = self.client.get("/tasks/", headers=headers)
        for task in response.json():
            self.assertEqual(task.get("user_id"), userid)
            
        
    @patch("mainMySQL.verify_token")
    def test_post_task_success(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        jsonbody_req = {
            "title": "New Task",
            "description": "Complete the test cases for the project.",
            "due_date": "2023-11-15T17:00:00Z",
            "priority": 2,
            "category_id": 3
        }
        response = self.client.post("/tasks/", headers=headers, json=jsonbody_req)
        self.assertEqual(response.status_code, 201)
        self.assertIn("task_id", response.json())  # Verify task ID is returned

    # Test 400 Bad Request for missing required fields in POST
    @patch("mainMySQL.verify_token")
    def test_post_task_missing_fields(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        incomplete_json = {
            "description": "Incomplete task data",
            "priority": 2
        }
        response = self.client.post("/tasks/", headers=headers, json=incomplete_json)
        self.assertEqual(response.status_code, 500)


    @patch("mainMySQL.verify_token")
    def test_delete_task_forbidden(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        response = self.client.delete("/tasks/1", headers=headers)
        self.assertEqual(response.status_code, 500)


    # Test PUT to update task with valid data and auth
    @patch("mainMySQL.verify_token")
    def test_update_task(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        
        updated_task_data = {
            "title": "Updated Task",
            "description": "Finalize and submit the comprehensive project plan document for approval.",
            "due_date": "2023-11-15T17:00:00Z",
            "priority": 2,
            "category_id": 3
        }

        response = self.client.put("/tasks/26", headers=headers, json=updated_task_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("title"), "Updated Task")

    # Test 404 Not Found if updating a non-existent task
    @patch("mainMySQL.verify_token")
    def test_update_nonexistent_task(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        updated_task_data = {
            "title": "Nonexistent Task",
            "description": "Trying to update a non-existent task."
        }
        response = self.client.put("/tasks/9999", headers=headers, json=updated_task_data)
        self.assertEqual(response.status_code, 422)

    #Test 401 Unauthorized when updating a task without auth
    def test_update_task_no_auth(self):
        updated_task_data = {
            "title": "Unauthorized Update",
            "description": "Trying to update without authentication."
        }
        response = self.client.put("/tasks/26", json=updated_task_data)
        self.assertEqual(response.status_code, 401)

    # Test 404 Not Found for GET non-existent task
    @patch("mainMySQL.verify_token")
    def test_get_nonexistent_task(self, mock_verify_token):
        mock_verify_token.return_value = True
        headers = {"Authorization": f"Bearer {self.mock_token}"}
        response = self.client.get("/tasks/9999", headers=headers)
        self.assertEqual(response.status_code, 404)
            
if __name__ == "__main__":
    unittest.main()

