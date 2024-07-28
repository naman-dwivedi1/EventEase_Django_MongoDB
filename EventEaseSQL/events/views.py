from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Event,EventApproval,PendingEvents
from django.utils import timezone
from datetime import datetime
import json
import jwt
import os
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import User
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger("events.views")

load_dotenv()

def get_user_role_from_jwt(request):
    token = request.headers.get('Authorization')
    if not token:
        return None
    try:
        token = token.split(" ")[1]
        decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECRET_ALGORITHM')])
        return decoded_token.get('role')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def categorize_events(events):
    upcoming_events = []
    past_events = []
    current_datetime = datetime.utcnow()

    for event in events:
        event_date = datetime.strptime(event.date, '%Y-%m-%d').date()
        event_time = datetime.strptime(event.time, '%H:%M:%S').time()
        event_datetime = datetime.combine(event_date, event_time)
        
        if event_datetime > current_datetime:
            upcoming_events.append(event)
        else:
            past_events.append(event)
            
    return upcoming_events, past_events

def display_events(request):
    
    logger.info("This is an informational message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    
    if request.method == 'GET':
        event_id = request.GET.get('id', '')
        if event_id == '':
            events = Event.objects.all()
            upcoming_events, past_events = categorize_events(events)
            return JsonResponse({'upcoming_events': [event.to_dict() for event in upcoming_events], 
                                 'past_events': [event.to_dict() for event in past_events]}, status=200)
        else:
            try:
                event = Event.objects.get(id=event_id)
                return JsonResponse({'event': event.to_dict()}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Event not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['GET'])

def event(request):
    user_role = get_user_role_from_jwt(request)
    
    if request.method == "POST":
        if user_role != "ADMIN":
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        
        if 'title' not in data:
            return JsonResponse({'error': 'Please provide title'}, status=400)
        else:
            title=data.get('title')
            if title.isdigit():
                return JsonResponse({'error': 'Title should not be a number'}, status=400)
            elif len(title)<5:
                return JsonResponse({'error': 'Title length can not be less than 5'}, status=400)
            elif len(title)>20:
                return JsonResponse({'error': 'Title length can not be greater than 20'}, status=400)
        
        if 'description' not in data:
            return JsonResponse({'error': 'Please provide description'}, status=400)
        else:
            description=data.get('description')
            if description.isdigit():
                return JsonResponse({'error': 'Description should not be a number'}, status=400)
            elif len(description)<10:
                return JsonResponse({'error': 'Description length can not be less than 10'}, status=400)
            elif len(description)>100:
                return JsonResponse({'error': 'Description length can not be greater than 100'}, status=400)
        
        if 'venue' not in data:
            return JsonResponse({'error': 'Please provide venue'}, status=400)
        else:
            venue=data.get('venue')
            if venue.isdigit():
                return JsonResponse({'error': 'Venue should not be a number'}, status=400)
            elif len(venue)<4:
                return JsonResponse({'error': 'Venue length can not be less than 4'}, status=400)
            elif len(venue)>100:
                return JsonResponse({'error': 'Venue length can not be greater than 100'}, status=400)
            
        if 'date' not in data:
            return JsonResponse({'error': 'Please provide date'}, status=400)
        
        if 'time' not in data:
            return JsonResponse({'error': 'Please provide time'}, status=400)
        
        current_datetime = datetime.utcnow()
        try:
            event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except:
            return JsonResponse({'error': 'Please provide date in this format yyyy-dd-mm'}, status=400)
        
        try:
            event_time = datetime.strptime(data['time'], '%H:%M:%S').time()
        except:
            return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
        
        event_datetime = datetime.combine(event_date, event_time)
        if event_datetime <= current_datetime:
            return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
        
        event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            date=data['date'],
            time=data['time'],
            organizer=data['organizer']
        )
        event.save()
        return JsonResponse({'message': 'Event registered successfully'}, status=201)
        
    elif request.method == 'PUT':
        if user_role != "ADMIN":
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        event_id = data.get('event_id')
        if not event_id:
            return JsonResponse({'error': 'Event ID is required'}, status=400)
        
        try:
            prev_event=Event.objects.get(id=event_id)
        except:
            return JsonResponse({'error': 'Event not found'}, status=404)
        
        if 'title' not in data:
            pass
        else:
            title=data.get('title')
            if title.isdigit():
                return JsonResponse({'error': 'Title should not be a number'}, status=400)
            elif len(title)<5:
                return JsonResponse({'error': 'Title length can not be less than 5'}, status=400)
            elif len(title)>20:
                return JsonResponse({'error': 'Title length can not be greater than 20'}, status=400)
        
        if 'description' not in data:
            pass
        else:
            description=data.get('description')
            if description.isdigit():
                return JsonResponse({'error': 'Description should not be a number'}, status=400)
            elif len(description)<10:
                return JsonResponse({'error': 'Description length can not be less than 10'}, status=400)
            elif len(description)>100:
                return JsonResponse({'error': 'Description length can not be greater than 100'}, status=400)
        
        if 'venue' not in data:
            pass
        else:
            venue=data.get('venue')
            if venue.isdigit():
                return JsonResponse({'error': 'Venue should not be a number'}, status=400)
            elif len(venue)<4:
                return JsonResponse({'error': 'Venue length can not be less than 4'}, status=400)
            elif len(venue)>100:
                return JsonResponse({'error': 'Venue length can not be greater than 100'}, status=400)
            
        
        if 'date' in data and 'time' in data:
            current_datetime = datetime.utcnow()
            try:
                event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except:
                return JsonResponse({'error': 'Please provide date in this format yyyy-dd-mm'}, status=400)
        
            try:
                event_time = datetime.strptime(data['time'], '%H:%M:%S').time()
            except:
                return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
            
            event_datetime = datetime.combine(event_date, event_time)
            if event_datetime <= current_datetime:
                return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
            
        elif 'date' in data and 'time' not in data:
            current_datetime = datetime.utcnow()
            try:
                event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except:
                return JsonResponse({'error': 'Please provide date in this format yyyy-dd-mm'}, status=400)
        
            event_time = datetime.strptime(prev_event.time, '%H:%M:%S').time()
            event_datetime = datetime.combine(event_date, event_time)
            if event_datetime <= current_datetime:
                return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
            
        elif 'time' in data and 'date' not in data:
            current_datetime = datetime.utcnow()
            try:
                event_date = datetime.strptime(prev_event.date, '%Y-%m-%d').date()
            except: return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
            
            try:
                event_time = datetime.strptime(data['time'], '%H:%M:%S').time()
            except:
                return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
            
            event_datetime = datetime.combine(event_date, event_time)
            if event_datetime <= current_datetime:
                return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
        update_data = {k: v for k, v in data.items() if k != 'event_id'}
        Event.objects.filter(id=event_id).update(**update_data)
        return JsonResponse({'message': 'Event updated successfully'}, status=200)

    elif request.method == 'DELETE':
        if user_role != "ADMIN":
            return JsonResponse({'error': 'Permission denied'}, status=403)
        data = json.loads(request.body)
        event_id = data.get('event_id')
        if not event_id:
            return JsonResponse({'error': 'Event ID is required'}, status=400)
        event = Event.objects.filter(id=event_id).delete()
        if event[0] == 1:
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Event not found'}, status=404)
    
    else:
        return HttpResponseNotAllowed(['POST', 'PUT', 'DELETE'])

def userevent(request):
    user_role = get_user_role_from_jwt(request)
    if request.method == 'POST':
        if user_role != "USER":
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        user_id = request.GET.get('id', '')
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        
        data = json.loads(request.body)
        
        if 'title' not in data:
            return JsonResponse({'error': 'Please provide title'}, status=400)
        else:
            title=data.get('title')
            if title.isdigit():
                return JsonResponse({'error': 'Title should not be a number'}, status=400)
            elif len(title)<5:
                return JsonResponse({'error': 'Title length can not be less than 5'}, status=400)
            elif len(title)>20:
                return JsonResponse({'error': 'Title length can not be greater than 20'}, status=400)
        
        if 'description' not in data:
            return JsonResponse({'error': 'Please provide description'}, status=400)
        else:
            description=data.get('description')
            if description.isdigit():
                return JsonResponse({'error': 'Description should not be a number'}, status=400)
            elif len(description)<10:
                return JsonResponse({'error': 'Description length can not be less than 10'}, status=400)
            elif len(description)>100:
                return JsonResponse({'error': 'Description length can not be greater than 100'}, status=400)
        
        if 'venue' not in data:
            return JsonResponse({'error': 'Please provide venue'}, status=400)
        else:
            venue=data.get('venue')
            if venue.isdigit():
                return JsonResponse({'error': 'Venue should not be a number'}, status=400)
            elif len(venue)<4:
                return JsonResponse({'error': 'Venue length can not be less than 4'}, status=400)
            elif len(venue)>100:
                return JsonResponse({'error': 'Venue length can not be greater than 100'}, status=400)
            
        if 'date' not in data:
            return JsonResponse({'error': 'Please provide date'}, status=400)
        
        if 'time' not in data:
            return JsonResponse({'error': 'Please provide time'}, status=400)
        
        current_datetime = datetime.utcnow()
        try:
            event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except:
            return JsonResponse({'error': 'Please provide date in this format yyyy-dd-mm'}, status=400)
    
        try:
            event_time = datetime.strptime(data['time'], '%H:%M:%S').time()
        except:
            return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
        
        event_datetime = datetime.combine(event_date, event_time)
        if event_datetime <= current_datetime:
            return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
        
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
            user_id=int(user_id),
            action="post",
            created_at=datetime.utcnow()
        )
        
        approval_request.save()
        return JsonResponse({'message': 'Event posted successfully. Awaiting admin approval.'}, status=201)
        
    elif request.method == 'PUT':
        if user_role != "USER":
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        
        event_id = data.get('event_id')
        user_id = data.get('user_id')
        
        if not event_id:
            return JsonResponse({'error': 'Event ID is required'}, status=400)
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        
        try:
            event=Event.objects.get(id=event_id)
        except:
            return JsonResponse({'error': 'Event not found'}, status=404)
        
        if 'title' not in data:
            pass
        else:
            title=data.get('title')
            if title.isdigit():
                return JsonResponse({'error': 'Title should not be a number'}, status=400)
            elif len(title)<5:
                return JsonResponse({'error': 'Title length can not be less than 5'}, status=400)
            elif len(title)>20:
                return JsonResponse({'error': 'Title length can not be greater than 20'}, status=400)
        
        if 'description' not in data:
            pass
        else:
            description=data.get('description')
            if description.isdigit():
                return JsonResponse({'error': 'Description should not be a number'}, status=400)
            elif len(description)<10:
                return JsonResponse({'error': 'Description length can not be less than 10'}, status=400)
            elif len(description)>100:
                return JsonResponse({'error': 'Description length can not be greater than 100'}, status=400)
        
        if 'venue' not in data:
            pass
        else:
            venue=data.get('venue')
            if venue.isdigit():
                return JsonResponse({'error': 'Venue should not be a number'}, status=400)
            elif len(venue)<4:
                return JsonResponse({'error': 'Venue length can not be less than 4'}, status=400)
            elif len(venue)>100:
                return JsonResponse({'error': 'Venue length can not be greater than 100'}, status=400)
        
        if 'date' in data and 'time' in data:
            current_datetime = datetime.utcnow()
            try:
                event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except:
                return JsonResponse({'error': 'Please provide date in this format yyyy-dd-mm'}, status=400)
        
            try:
                event_time = datetime.strptime(data['time'], '%H:%M:%S').time()
            except:
                return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
            
            event_datetime = datetime.combine(event_date, event_time)
            if event_datetime <= current_datetime:
                return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
            
        elif 'date' in data and 'time' not in data:
            current_datetime = datetime.utcnow()
            try:
                event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except:
                return JsonResponse({'error': 'Please provide date in this format yyyy-dd-mm'}, status=400)
        
            event_time = datetime.strptime(event.time, '%H:%M:%S').time()
            event_datetime = datetime.combine(event_date, event_time)
            if event_datetime <= current_datetime:
                return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)
            
        elif 'time' in data and 'date' not in data:
            current_datetime = datetime.utcnow()
            try:
                event_date = datetime.strptime(event.date, '%Y-%m-%d').date()
            except: return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
            
            try:
                event_time = datetime.strptime(data['time'], '%H:%M:%S').time()
            except:
                return JsonResponse({'error': 'Please provide time in this format hours:minutes:seconds'}, status=400)
            
            event_datetime = datetime.combine(event_date, event_time)
            if event_datetime <= current_datetime:
                return JsonResponse({'error': 'Please provide appropriate time for the event'}, status=400)

        if event.organizer == user_id:
            pending_event = PendingEvents(
                event_id=event.id,
                title=event.title,
                description=event.description,
                venue=event.venue,
                date=event.date,
                time=event.time,
                organizer=event.organizer,
            )
            update_data = {k: v for k, v in data.items() if k not in ['user_id', 'event_id']}
            for key, value in update_data.items():
                setattr(pending_event, key, value)
            update_data = {k: v for k, v in data.items() if k not in ['user_id', 'event_id']}
            
            pending_event.save()
            
            approval_request = EventApproval(
                event_id=int(pending_event.id),
                user_id=int(user_id),
                action='put'
            )
            approval_request.save()
            
            return JsonResponse({'message': 'Update request submitted. Awaiting admin approval.'}, status=200)
        else:
            return JsonResponse({'error': 'User not authorized'}, status=403)
        
    elif request.method == 'DELETE':
        if user_role != 'USER':
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        event_id = data.get('event_id')
        user_id = data.get('user_id')
        
        if not event_id:
            return JsonResponse({'error': 'Event ID is required'}, status=400)
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
         
        event = Event.objects.filter(id=event_id).first()
        if event:
            pass  
        else:
            return JsonResponse({'error':"Event not found"},status=404)
        
        if event.organizer == user_id:
            approval_request = EventApproval(
                event_id=int(event_id),
                user_id=int(user_id),
                action='delete'
            )
            approval_request.save()
            
            return JsonResponse({'message': 'Delete request submitted. Awaiting admin approval.'}, status=200)
        else:
            return JsonResponse({'error': 'User not authorized.'}, status=403)
            
    else:
        return HttpResponseNotAllowed(['POST', 'PUT', 'DELETE'])
        
def admin_approve_event(request):
    user_role = get_user_role_from_jwt(request)
    if user_role != "ADMIN":
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        approval_id = data.get('approval_id')
        action = data.get('action')  # 'approve' or 'reject'
        
        if not approval_id:
            return JsonResponse({'error': 'Approval ID is required'}, status=400)
        if not action:
            return JsonResponse({'error': 'Action is required (approve/reject)'}, status=400)
        
        try:
            approval_request = EventApproval.objects.get(id=approval_id)
            
            if approval_request.action == 'post':
                if action == 'approve':
                    event = PendingEvents.objects.get(id=approval_request.event_id)
                    nevent=Event(
                        title=event.title,
                        description=event.description,
                        venue=event.venue,
                        date=event.date,
                        time=event.time,
                        organizer=event.organizer,
                    )
                    nevent.save()
                    event.delete()
                    EventApproval.objects.filter(id=approval_id).update(approved=True)    
                else:
                    PendingEvents.objects.filter(id=approval_request.event_id).delete()
                    EventApproval.objects.filter(id=approval_id).update(approved=False)
                    
            elif approval_request.action == 'put':
                if action == 'approve':
                    event = PendingEvents.objects.get(id=approval_request.event_id)
                    Event.objects.filter(id=event.event_id).update(
                        title=event.title,
                        description=event.description,
                        venue=event.venue,
                        date=event.date,
                        time=event.time,
                        organizer=event.organizer,
                    )
                    event.delete()
                    EventApproval.objects.filter(id=approval_id).update(approved=True)    
                else:
                    PendingEvents.objects.filter(id=approval_request.event_id).delete()
                    EventApproval.objects.filter(id=approval_id).update(approved=False)
                    
            elif approval_request.action == 'delete':
                if action == 'approve':
                    Event.objects.filter(id=approval_request.event_id).delete()
                    EventApproval.objects.filter(id=approval_id).update(approved=True)
                else:
                    EventApproval.objects.filter(id=approval_id).update(approved=False)
                    
            else:
                return JsonResponse({'error': 'Unknown action type'}, status=400)
                
            if action == 'approve': return JsonResponse({'message': f'Request approved for {approval_request.event_id}.'}, status=200)
            else : return JsonResponse({'message': f'Request approved for {approval_request.event_id}.'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Approval request not found.'}, status=404)
        
    return HttpResponseNotAllowed(['POST'])

def register_event(request):
    if request.method == 'POST':
        user_role = get_user_role_from_jwt(request)
        if user_role != 'USER':
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        event_id = data.get('event_id')
        user_id = data.get('user_id')
        if not event_id or not user_id:
            return JsonResponse({'error': 'Event ID and User ID are required'}, status=400)
        
        try:
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(User, id=user_id)
            event.attendees.add(user)
            return JsonResponse({'message': 'User registered to event successfully'}, status=200)
        except: return JsonResponse({'error': 'Event not found or user already registered'}, status=404)
    return HttpResponseNotAllowed(['POST'])

def unregister_event(request):
    if request.method == 'POST':
        user_role = get_user_role_from_jwt(request)
        if user_role != 'USER':
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        event_id = data.get('event_id')
        user_id = data.get('user_id')
        if not event_id or not user_id:
            return JsonResponse({'error': 'Event ID and User ID are required'}, status=400)
        
        try:
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(User, id=user_id)
            event.attendees.remove(user)
            return JsonResponse({'message': 'User Unregistered to event successfully'}, status=200)
        except: return JsonResponse({'error': 'Event not found or user already unregistered'}, status=404)
    return HttpResponseNotAllowed(['POST'])
    
def event_attendees(request):
    if request.method == 'POST':
        user_role = get_user_role_from_jwt(request)
        if user_role != 'USER' and user_role != 'ADMIN':
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        event_id = data.get('event_id')
        
        if not event_id:
            return JsonResponse({'error': 'Event ID is required'}, status=400)
        
        try:
            event = Event.objects.get(id=event_id)
            attendees = event.attendees.all()
            attendees_list = [{'id': attendee.id, 'username': attendee.username} for attendee in attendees]
            return JsonResponse({'attendees': attendees_list}, status=200)
        except: return JsonResponse({'error': 'Event not found or user already unregistered'}, status=404)
    return HttpResponseNotAllowed(['POST'])
   
def user_events(request):
    if request.method == 'POST':
        user_role = get_user_role_from_jwt(request)
        if user_role != 'USER' and user_role != 'ADMIN':
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        if 'user_id' not in data:
            return JsonResponse({'error': 'Event ID and User ID are required'}, status=400)
        user_id = data['user_id']  
        try:
            user = get_object_or_404(User, id=user_id)
            events = user.events_attending.all()
            events_list=[{'id':event.id,'title':event.title} for event in events]
            return JsonResponse({'events': events_list}, status=200)
        except: return JsonResponse({'error': 'Event not found or user already unregistered'}, status=404)
    return HttpResponseNotAllowed(['POST'])