
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from todo_app.models import Todo
from todo_app.crypto import encrypt_text, decrypt_text

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')

    def test_rate_limiting(self):
        # Test login rate limiting
        for _ in range(6):
            response = self.client.post(reverse('login'), {'email': 'test@test.com', 'password': 'wrong'})
        self.assertEqual(response.status_code, 403)

    def test_authorization(self):
        # Create a todo for first user
        self.client.force_login(self.user)
        todo = Todo.objects.create(user=self.user, task='Test task')

        # Try to access with second user
        self.client.force_login(self.other_user)
        response = self.client.post(f'/todo_app/todo/{todo.id}/toggle/')
        self.assertEqual(response.status_code, 403)

    def test_encryption(self):
        test_text = "sensitive data"
        encrypted = encrypt_text(test_text)
        self.assertNotEqual(test_text, encrypted)
        decrypted = decrypt_text(encrypted)
        self.assertEqual(test_text, decrypted)