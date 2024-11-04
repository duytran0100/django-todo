from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todos.models import ToDo
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TodoAPITestCase(APITestCase):
    fixtures = ['todos/fixtures/todo.json']

    def setUp(self):
        """
        Set up method to prepare test environment.
        Loads todo fixtures, creates a test user, and generates an authentication token for the user.
        """
        user = User.objects.create_user(username='testuser', password='testpassword')
        token, created = Token.objects.get_or_create(user=user)
        self.token = token


    def tearDown(self):
        """
        Tear down method that deletes all the todo objects from the database after
        a test has been run.
        """
        return ToDo.objects.all().delete()
    
    def test_todo_list(self):
        """
        Test that the API returns the correct number of todos when the GET request
        is called on the todo-list endpoint.
        """
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        response = self.client.get(reverse('todo-list'), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data['count'], 4)  # Expecting 4 items from the fixture
        self.assertEqual(len(response_data['results']), 4) # Expecting 4 items from response

    def test_todo_list_with_limit(self):
        """
        Test that the API returns the correct number of todos when the GET request
        is called on the todo-list endpoint with a limit parameter.
        """
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        response = self.client.get(reverse('todo-list') + '?limit=2', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data['count'], 4)  # Expecting 4 items from the fixture
        self.assertEqual(len(response_data['results']), 2) # Expecting 1 items from response

    def test_todo_list_with_page(self):
        """
        Test that the API returns the correct number of todos when the GET request
        is called on the todo-list endpoint with an page parameter.
        """
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        response = self.client.get(reverse('todo-list') + '?limit=3&page=2', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data['count'], 4)  # Expecting 4 items from the fixture
        self.assertEqual(len(response_data['results']), 1) # Expecting 1 items from response

    def test_todo_create(self):
        """
        Test that the API creates a new todo item
        """
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        data = {
            'title': 'Test Todo',
            'description': 'Test description',
            'completed': False
        }
        response = self.client.post(reverse('todo-list'), data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data
        todo_id = response_data['id']
        created_todo = ToDo.objects.get(id=todo_id)
        self.assertEqual(created_todo.title, data['title'])
        self.assertEqual(created_todo.description, data['description'])
        self.assertEqual(created_todo.completed, data['completed'])

    def test_todo_create_with_invalid_data(self):
        """
        Test that the API creates a new todo item return error when invalid data is provided
        """
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        data = {
            'description': 'Test description',
            'completed': False
        }
        response = self.client.post(reverse('todo-list'), data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_todo_create_without_token(self):
        """
        Test that the API returns a 401 status code when no token is provided
        """
        data = {
            'title': 'Test Todo',
            'description': 'Test description',
            'completed': False
        }
        response = self.client.post(reverse('todo-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_todo_update(self):
        """
        Test that the API updates a todo item
        """
        todo = ToDo.objects.create(title='Test Todo', description='Test description', completed=False)
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        data = {
            'title': 'Updated Test Todo',
            'description': 'Updated Test description',
            'completed': True
        }
        response = self.client.put(reverse('todo-detail', args=[todo.id]), data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_todo = ToDo.objects.get(id=todo.id)
        self.assertEqual(updated_todo.title, data['title'])
        self.assertEqual(updated_todo.description, data['description'])
        self.assertEqual(updated_todo.completed, data['completed'])

    def test_todo_update_with_invalid_data(self):
        """
        Test that the API updates a todo item return error when invalid data is provided
        """
        todo = ToDo.objects.create(title='Test Todo', description='Test description', completed=False)
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        data = {
            'title': '', # Title can't be empty
            'description': 'Updated Test description',
            'completed': True
        }
        response = self.client.put(reverse('todo-detail', args=[todo.id]), data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_todo_update_without_token(self):
        """
        Test that the API returns a 401 status code when no token is provided
        """
        todo = ToDo.objects.create(title='Test Todo', description='Test description', completed=False)
        data = {
            'title': 'Updated Test Todo',
            'description': 'Updated Test description',
            'completed': True
        }
        response = self.client.put(reverse('todo-detail', args=[todo.id]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_todo_update_with_not_exist_id(self):
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        data = {
            'title': 'Updated Test Todo',
            'description': 'Updated Test description',
            'completed': True
        }
        response = self.client.put(reverse('todo-detail', args=[999]), data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_todo_delete(self):
        """
        Test that the API deletes a todo item
        """
        todo = ToDo.objects.create(title='Test Todo', description='Test description', completed=False)
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        response = self.client.delete(reverse('todo-detail', args=[todo.id]), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ToDo.DoesNotExist):
            ToDo.objects.get(id=todo.id)
    
    def test_todo_delete_without_token(self):
        """
        Test that the API returns a 401 status code when no token is provided
        """
        todo = ToDo.objects.create(title='Test Todo', description='Test description', completed=False)
        response = self.client.delete(reverse('todo-detail', args=[todo.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_todo_delete_with_not_exist_id(self):
        headers = {
            'Authorization': 'Token {}'.format(self.token.key)
        }
        response = self.client.delete(reverse('todo-detail', args=[999]), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)