from datetime import datetime
import pytest
from django.urls import reverse
from django.test import Client
from authentication.models import User
import json
from .models import Event, PendingEvents, EventApproval
from django.http import HttpResponseNotAllowed

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def admin_user():
    return User.create_user(
        username = 'admin',
        email = 'admin@gmail.com',
        password = 'adminpassword',
        role = 'ADMIN'
    )

@pytest.fixture
def regular_user():
    return User.create_user(
        email='user@example.com',
        username='user',
        password='userpassword',
        role='USER'
    )
    
# TOKEN VALIDATION
    
import jwt
import os

from events.views import get_user_role_from_jwt

@pytest.fixture
def mock_request(mocker):
    return mocker.Mock()

def test_get_user_role_from_jwt_valid_token(mock_request, mocker):
    mock_request.headers = {'Authorization': 'Bearer validtoken'}
    mock_decode = mocker.patch('events.views.jwt.decode')
    mock_decode.return_value = {'role': 'ADMIN'}
    
    role = get_user_role_from_jwt(mock_request)
    
    assert role == 'ADMIN'
    mock_decode.assert_called_once_with('validtoken', os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECRET_ALGORITHM')])

def test_get_user_role_from_jwt_no_token(mock_request):
    mock_request.headers = {}
    role = get_user_role_from_jwt(mock_request)
    assert role is None

def test_get_user_role_from_jwt_expired_token(mock_request, mocker):
    mock_request.headers = {'Authorization': 'Bearer expiredtoken'}
    mock_decode = mocker.patch('events.views.jwt.decode')
    mock_decode.side_effect = jwt.ExpiredSignatureError
    role = get_user_role_from_jwt(mock_request)
    assert role is None

def test_get_user_role_from_jwt_invalid_token(mock_request, mocker):
    mock_request.headers = {'Authorization': 'Bearer invalidtoken'}
    mock_decode = mocker.patch('events.views.jwt.decode')
    mock_decode.side_effect = jwt.InvalidTokenError
    
    role = get_user_role_from_jwt(mock_request)
    assert role is None
    
# GET
    
@pytest.mark.django_db
def test_get_events(client,admin_user):
    url = reverse('display_events')
    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2023-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event2 = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event2.save()
    
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_events_id_given(client,admin_user):
    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    url = f"{reverse('display_events')}?id={event.id}"
    
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_events_id_given_event_not_found(client,admin_user):
    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    url = f"{reverse('display_events')}?id={5}"
    
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_event_method_not_allowed(client):
    url = reverse('display_events')
    
    response = client.post(url)
    assert response.status_code == HttpResponseNotAllowed.status_code
    assert response['Allow'] == 'GET'

# ADMIN

# POST

@pytest.mark.django_db
def test_create_event_post(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 201
    assert json.loads(response.content) == {'message': 'Event registered successfully'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_create_event_post_wrong_date_format(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "12-12-2025",
        "time": "16:25:00",
        "organizer": admin_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide date in this format yyyy-dd-mm'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_create_event_post_wrong_time_format(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": admin_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide time in this format hours:minutes:seconds'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_create_event_inappropriate_time(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2023-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide appropriate time for the event'}
    mock_inner_function.assert_called_once()
    
    
@pytest.mark.django_db
def test_create_event_post_incorrect_user(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('event')

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
# PUT

@pytest.mark.django_db
def test_update_event_put(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Event updated successfully'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_update_event_put_wrong_date_format(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
        "title": "Demo Event",
        "date": "12-12-2025",
    }
    
    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide date in this format yyyy-dd-mm'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_update_event_put_wrong_time_format(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
        "time": "16:60:00",
    }
    
    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide time in this format hours:minutes:seconds'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_update_event_inappropriate_time(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
        "title": "Demo Event",
        "date": "2023-12-22",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide appropriate time for the event'}
    mock_inner_function.assert_called_once()
    
    
@pytest.mark.django_db
def test_create_event_put_incorrect_user(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_put_event_id_not_given(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:50:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Event ID is required'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_update_event_put_event_not_found(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":5,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Event not found'}
    mock_inner_function.assert_called_once()

# DELETE

@pytest.mark.django_db
def test_update_event_delete(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Event deleted successfully'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_create_event_delete_incorrect_user(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_delete_event_id_not_given(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:50:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Event ID is required'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_update_event_delete_event_not_found(client, admin_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": admin_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":5,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Event not found'}
    mock_inner_function.assert_called_once()
    

# USER

@pytest.mark.django_db
def test_create_event_post_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    user_id = regular_user.id
    url = f"{reverse('userevent')}?id={user_id}"
    
    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 201
    assert json.loads(response.content) == {'message': 'Event posted successfully. Awaiting admin approval.'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_create_event_post_wrong_date_format_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    user_id = regular_user.id
    url = f"{reverse('userevent')}?id={user_id}"

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "12-12-2025",
        "time": "16:25:00",
        "organizer": regular_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide date in this format yyyy-dd-mm'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_create_event_post_wrong_time_format_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    user_id = regular_user.id
    url = f"{reverse('userevent')}?id={user_id}"

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": regular_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide time in this format hours:minutes:seconds'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_create_event_inappropriate_time_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    user_id = regular_user.id
    url = f"{reverse('userevent')}?id={user_id}"

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2023-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide appropriate time for the event'}
    mock_inner_function.assert_called_once()
    
    
@pytest.mark.django_db
def test_create_event_post_incorrect_user_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    user_id = regular_user.id
    url = f"{reverse('userevent')}?id={user_id}"

    event_data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }

    response = client.post(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
# PUT

@pytest.mark.django_db
def test_update_event_put_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url=reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Update request submitted. Awaiting admin approval.'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_update_event_put_wrong_date_format_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')
    
    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
        "title": "Demo Event",
        "date": "12-12-2025",
    }
    
    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide date in this format yyyy-dd-mm'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_update_event_put_wrong_time_format_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
        "time": "16:60:00",
    }
    
    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide time in this format hours:minutes:seconds'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_update_event_inappropriate_time_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
        "title": "Demo Event",
        "date": "2023-12-22",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Please provide appropriate time for the event'}
    mock_inner_function.assert_called_once()
    
    
@pytest.mark.django_db
def test_create_event_put_incorrect_user_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_put_event_id_not_given_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:50:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Event ID is required'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_put_user_id_not_given_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:50:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'User ID is required'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_update_event_put_event_not_found_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":5,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Event not found'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_put_user_not_authorized_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":5,
        "event_id":event.id,
        "title": "Demo Event",
    }

    response = client.put(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'User not authorized'}
    mock_inner_function.assert_called_once()


# DELETE

@pytest.mark.django_db
def test_update_event_delete_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Delete request submitted. Awaiting admin approval.'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_create_event_delete_incorrect_user_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
        "event_id":event.id,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_delete_event_id_not_given_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:50:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "user_id":regular_user.id,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Event ID is required'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_delete_user_id_not_given_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:50:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'User ID is required'}
    mock_inner_function.assert_called_once()


@pytest.mark.django_db
def test_update_event_delete_event_not_found_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":6,
        "user_id":regular_user.id
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Event not found'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_update_event_delete_user_not_authorized_user(client, regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('userevent')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:60:00",
        "organizer": regular_user.id
    }
    
    event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date=data['date'],
        time=data['time'],
        organizer=data['organizer']
    )
    event.save()
    
    event_data = {
        "event_id":event.id,
        "user_id":5
    }

    response = client.delete(url, data=json.dumps(event_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'User not authorized.'}
    mock_inner_function.assert_called_once()
    
# ADMIN_APPROVALS

@pytest.mark.django_db
def test_admin_approval(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('admin_approve_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = PendingEvents(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    approval_request = EventApproval(
            event_id=int(event.id),
            user_id=int(regular_user.id),
            action="post",
            created_at=datetime.utcnow()
        )
                
    approval_request.save()
    
    approval_data={
        "approval_id":approval_request.id,
        "action":"approve"
    }

    response = client.post(url, data=json.dumps(approval_data), content_type='application/json')
    assert response.status_code == 200
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_admin_approval_incorrect_user(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('admin_approve_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = PendingEvents(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    approval_request = EventApproval(
            event_id=int(event.id),
            user_id=int(regular_user.id),
            action="post",
            created_at=datetime.utcnow()
        )
                
    approval_request.save()
    
    approval_data={
        "approval_id":approval_request.id,
        "action":"approve"
    }

    response = client.post(url, data=json.dumps(approval_data), content_type='application/json')
    assert response.status_code == 403
    assert json.loads(response.content) == {'error': 'Permission denied'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_admin_approval_approval_id_not_given(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('admin_approve_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = PendingEvents(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    approval_request = EventApproval(
            event_id=int(event.id),
            user_id=int(regular_user.id),
            action="post",
            created_at=datetime.utcnow()
        )
                
    approval_request.save()
    
    approval_data={
        "action":"approve"
    }

    response = client.post(url, data=json.dumps(approval_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Approval ID is required'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_admin_approval_action_not_given(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('admin_approve_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = PendingEvents(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    approval_request = EventApproval(
            event_id=int(event.id),
            user_id=int(regular_user.id),
            action="post",
            created_at=datetime.utcnow()
        )
                
    approval_request.save()
    
    approval_data={
        "approval_id":approval_request.id,
    }

    response = client.post(url, data=json.dumps(approval_data), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Action is required (approve/reject)'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_admin_approval_incorrect_approval_id(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="ADMIN")
    url = reverse('admin_approve_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = PendingEvents(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    approval_request = EventApproval(
            event_id=int(event.id),
            user_id=int(regular_user.id),
            action="post",
            created_at=datetime.utcnow()
        )
                
    approval_request.save()
    
    approval_data={
        "approval_id":5,
        "action":"approve"
    }

    response = client.post(url, data=json.dumps(approval_data), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Approval request not found.'}
    mock_inner_function.assert_called_once()

# event_registering

@pytest.mark.django_db
def test_event_registering(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('register_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "event_id":event.id,
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'User registered to event successfully'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_event_registering_event_id_not_given(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('register_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Event ID and User ID are required'}
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_event_registering_event_not_found(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('register_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "event_id":5,
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Event not found or user already registered'}
    mock_inner_function.assert_called_once()
    
# event_unregistering

@pytest.mark.django_db
def test_event_unregistering(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('unregister_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "event_id":event.id,
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'User Unregistered to event successfully'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_event_unregistering_event_id_not_given(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('unregister_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {'error': 'Event ID and User ID are required'}
    mock_inner_function.assert_called_once()

@pytest.mark.django_db
def test_event_unregistering_event_not_found(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('unregister_event')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "event_id":5,
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 404
    assert json.loads(response.content) == {'error': 'Event not found or user already unregistered'}
    mock_inner_function.assert_called_once()
    
# getting attendees for an event

@pytest.mark.django_db
def test_event_attendess(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('event_attendees')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "event_id":event.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 200
    mock_inner_function.assert_called_once()
    
@pytest.mark.django_db
def test_user_events(client, admin_user,regular_user,mocker):
    mock_inner_function = mocker.patch('events.views.get_user_role_from_jwt', return_value="USER")
    url = reverse('user_events')

    data = {
        "title": "Demo Event",
        "description": "This is a demo event.",
        "venue": "Pune",
        "date": "2025-12-22",
        "time": "16:25:00",
        "organizer": admin_user.id
    }
    
    event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
    event.save()
    
    request={
        "user_id":regular_user.id
    }

    response = client.post(url, data=json.dumps(request), content_type='application/json')
    assert response.status_code == 200
    mock_inner_function.assert_called_once()