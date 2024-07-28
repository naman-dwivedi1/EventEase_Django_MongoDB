import pytest
from django.urls import reverse
from django.test import Client
from django.http import HttpResponseNotAllowed
from authentication.models import User
import json

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user_data():
    return {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'password123'
    }

@pytest.fixture
def create_user(user_data):
    user = User(email=user_data['email'], username=user_data['username'])
    user.set_password(user_data['password'])
    user.save()
    return user

@pytest.mark.django_db
def test_signup_success(client, user_data):
    url = reverse('signup')
    response = client.post(url, json.dumps(user_data), content_type='application/json')
    assert response.status_code == 201
    assert User.objects.filter(email=user_data['email']).exists()
    
@pytest.mark.django_db
def test_signup_success_wrong_method(client, user_data):
    url = reverse('signup')
    response = client.put(url, json.dumps(user_data), content_type='application/json')
    assert response.status_code == HttpResponseNotAllowed.status_code
    assert response['Allow'] == 'POST'

@pytest.mark.django_db
def test_signup_missing_fields(client):
    url = reverse('signup')
    response = client.post(url, json.dumps({'email': 'test@example.com'}), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == {'error': 'Email, username, and password are required'}

@pytest.mark.django_db
def test_signup_existing_email(client, create_user):
    url = reverse('signup')
    user_data = {
        'email': 'testuser@example.com',
        'username': 'newuser',
        'password': 'password123'
    }
    response = client.post(url, json.dumps(user_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == {'error': 'Email already exists'}
    
@pytest.mark.django_db
def test_signin_success(client, create_user, user_data):
    url = reverse('signin')
    response = client.post(url, json.dumps({
        'email': user_data['email'],
        'password': user_data['password']
    }), content_type='application/json')
    assert response.status_code == 200
    assert 'token' in response.json()
    
@pytest.mark.django_db
def test_signin_success_wrong_method(client, create_user, user_data):
    url = reverse('signin')
    response = client.put(url, json.dumps({
        'email': user_data['email'],
        'password': user_data['password']
    }), content_type='application/json')
    assert response.status_code == HttpResponseNotAllowed.status_code
    assert response['Allow'] == 'POST'

@pytest.mark.django_db
def test_signin_missing_fields(client):
    url = reverse('signin')
    response = client.post(url, json.dumps({'email': 'test@example.com'}), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == {'error': 'Email and password are required'}

@pytest.mark.django_db
def test_signin_invalid_credentials(client, user_data):
    user=User(email=user_data['email'], username=user_data['username'])
    user.set_password('wrongpassword')
    user.save()
    url = reverse('signin')
    response = client.post(url, json.dumps({
        'email': user_data['email'],
        'password': 'incorrectpassword'
    }), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid credentials'}
    
@pytest.mark.django_db
def test_signin_user_does_not_exists(client, user_data):
    url = reverse('signin')
    response = client.post(url, json.dumps({
        'email': user_data['email'],
        'password': user_data['password']
    }), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == {'error': 'User with this email does not exists'}