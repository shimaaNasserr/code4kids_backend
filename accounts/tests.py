from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User


class RoleLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create users for each role
        self.admin = User.objects.create_user(
            email='admin@example.com', username='admin', role='Admin', password='Admin123!'
        )
        self.admin.is_superuser = True
        self.admin.is_staff = True
        self.admin.save()

        self.parent = User.objects.create_user(
            email='parent@example.com', username='parent', role='Parent', password='Parent123!'
        )

        self.kid = User.objects.create_user(
            email='kid@example.com', username='kid', role='Kid', password='Kid123!'
        )

    def test_admin_login_success(self):
        url = '/api/accounts/admin/login'
        resp = self.client.post(url, {'email': 'admin@example.com', 'password': 'Admin123!'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        self.assertEqual(resp.data['user']['role'], 'Admin')

    def test_admin_login_reject_non_superuser(self):
        # Demote admin
        self.admin.is_superuser = False
        self.admin.save()
        url = '/api/accounts/admin/login'
        resp = self.client.post(url, {'email': 'admin@example.com', 'password': 'Admin123!'}, format='json')
        self.assertEqual(resp.status_code, 401)

    def test_parent_login_success(self):
        url = '/api/accounts/parent/login'
        resp = self.client.post(url, {'email': 'parent@example.com', 'password': 'Parent123!'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['user']['role'], 'Parent')

    def test_kid_login_success(self):
        url = '/api/accounts/kid/login'
        resp = self.client.post(url, {'email': 'kid@example.com', 'password': 'Kid123!'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['user']['role'], 'Kid')

    def test_role_mismatch_rejected(self):
        # Try kid using parent endpoint
        url = '/api/accounts/parent/login'
        resp = self.client.post(url, {'email': 'kid@example.com', 'password': 'Kid123!'}, format='json')
        self.assertEqual(resp.status_code, 401)

# Create your tests here.
