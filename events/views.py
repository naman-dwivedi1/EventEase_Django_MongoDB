from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import event_collection, Event , approval_collection , EventApproval, pending_events_collection
import json
from bson import ObjectId
import jwt
import os 
from dotenv import load_dotenv
from authentication.models import user_collection
from datetime import datetime

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
    current_time = datetime.utcnow()

    for event in events:
        event_date = datetime.strptime(event['date'], '%Y-%m-%d')
        event_time = datetime.strptime(event['time'], '%H:%M:%S').time()
        event_datetime = datetime.combine(event_date, event_time)
        
        if event_datetime > current_time:
            upcoming_events.append(event)
        else:
            past_events.append(event)

    return upcoming_events, past_events


    
def display_events(request):
    if request.method=='GET':
        id=request.GET.get('id', '')
        if(id==''):
            try:
                events = list(event_collection.find({}, {'_id': 0}))
                upcoming_events, past_events = categorize_events(events)
                upcoming_events, past_events = categorize_events(events)
                return JsonResponse({'upcoming_events': upcoming_events, 'past_events': past_events}, status=200)
            except Exception as e:
                return JsonResponse({'error': 'Internal Server Error, Failed to fetch the event with this id'}, status=500)
        else:
            try:
                event = event_collection.find_one({'_id': ObjectId(id)}, {'_id': 0})
                return JsonResponse({'event': event}, status=200)
            except Exception as e:
                return JsonResponse({'error': 'Internal Server Error, Failed to fetch events'}, status=500)
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
    
def event(request):
    try:
        user_role = get_user_role_from_jwt(request)
        
        if request.method == "POST":
            if user_role != "ADMIN":
                return JsonResponse({'error': 'Permission denied'}, status=403)
            
            try:
                data = json.loads(request.body)
                nevent=Event(title=data['title'],description=data['description'],venue=data['venue'],date=data['date'],time=data['time'],organizer=data['organizer'])
                nevent=nevent.to_dict()
                result = event_collection.insert_one(nevent)
                if result.inserted_id:
                    return JsonResponse({'message': 'Event registered successfully'}, status=201)
                else:
                    return JsonResponse({'error': 'Failed to register event'}, status=500)
            except Exception as e:
                return JsonResponse({'error': 'Internal Sever Error'}, status=500)
            
        elif request.method == 'PUT':
            if user_role != "ADMIN":
                return JsonResponse({'error': 'Permission denied'}, status=403)
            
            try:
                data = json.loads(request.body)
                event_id = data.get('id')
                if not event_id:
                    return JsonResponse({'error': 'Event ID is required'}, status=400)

                update_data = {k: v for k, v in data.items() if k != 'id'}
                updated_event = event_collection.find_one_and_update(
                    {'_id': ObjectId(event_id)},
                    {'$set': update_data},
                    return_document=True
                )

                if updated_event:
                    return JsonResponse({'message': 'Event updated successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'Event not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
        
        elif request.method == 'DELETE':
            if user_role != "ADMIN":
                return JsonResponse({'error': 'Permission denied'}, status=403)
            try:
                data = json.loads(request.body)
                event_id = data.get('id')
                if not event_id:
                    return JsonResponse({'error': 'Event ID is required'}, status=400)

                result = event_collection.delete_one({'_id': ObjectId(event_id)})
                if result.deleted_count == 1:
                    return JsonResponse({'message': 'Event deleted successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'Event not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
        
        else:
            return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
    except:
        return JsonResponse({'error': 'Internal Server Error'},status=500)

def userevent(request):
    try:
        user_role = get_user_role_from_jwt(request)
        
        if request.method == 'POST':
            if user_role != "USER":
                return JsonResponse({'error': 'Permission denied'}, status=403)
            
            user_id = request.POST.get('id','')
            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            
            data = json.loads(request.body)
            nevent=Event(title=data['title'],description=data['description'],venue=data['venue'],date=data['date'],time=data['time'],organizer=data['organizer'])
            nevent=nevent.to_dict()
            
            approval_request = EventApproval(
                event_id=str(pending_events_collection.insert_one(nevent).inserted_id),
                user_id=user_id,
                action='post'
            )
            result=approval_collection.insert_one(approval_request.to_dict())
            if result.inserted_id:
                return JsonResponse({'message': 'Event posted successfully. Awaiting admin approval.'}, status=201)
            else:
                return JsonResponse({'error': 'Failed to register event, Please try again'}, status=500)
            
        elif request.method=='PUT':
            if user_role != "USER":
                return JsonResponse({'error': 'Permission denied'}, status=403)
            
            try:
                data = json.loads(request.body)
                event_id = data.get('event_id')
                user_id=data.get('user_id')
                
                if not event_id:
                    return JsonResponse({'error': 'Event ID is required'}, status=400)
                if not user_id:
                    return JsonResponse({'error': 'User ID is required'}, status=400)

                event=event_collection.find_one({'_id': ObjectId(event_id)})
                
                if event and event['organizer']==user_id:
                    newevent=event.copy()
                    update_data = {k: v for k, v in data.items() if (k!='user_id' and k!='event_id')}
                    pending_events_collection.insert_one(newevent)
                    updated_event = pending_events_collection.find_one_and_update(
                        {'_id': ObjectId(event_id)},
                        {'$set': update_data},
                        return_document=True
                    )
                    approval_request = EventApproval(
                        event_id=event_id,
                        user_id=user_id,
                        action='put'
                    )
                    result=approval_collection.insert_one(approval_request.to_dict())
                    if updated_event and result.inserted_id:
                        return JsonResponse({'message': 'Update request submitted. Awaiting admin approval.'}, status=200)
                    else:
                        return JsonResponse({'error': 'Event not found'}, status=404)
                else: return JsonResponse({'error': 'Event not found or unauthorized.'}, status=403)
            except Exception as e:
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
            
        elif request.method == 'DELETE':
            user_role=get_user_role_from_jwt(request)
            if user_role!='USER': return JsonResponse({'error': 'Permission denied'}, status=403)
            
            try:
                data = json.loads(request.body)
                event_id = data['event_id']
                user_id=data['user_id']
                
                if not event_id:
                    return JsonResponse({'error': 'Event ID is required'}, status=400)
                if not user_id:
                    return JsonResponse({'error': 'User ID is required'}, status=400)
                 
                event = event_collection.find_one({'_id': ObjectId(event_id)})
                if event and event['organizer'] == user_id:
                    approval_request = EventApproval(
                        event_id=event_id,
                        user_id=user_id,
                        action='delete'
                    )
                    result=approval_collection.insert_one(approval_request.to_dict())
                    if result.inserted_id:
                        return JsonResponse({'message': 'Delete request submitted. Awaiting admin approval.'}, status=200)
                    else:
                        return JsonResponse({'error': 'Failed to put request, Please try again'},status=400)
                else:
                    return JsonResponse({'error': 'Event not found or unauthorized.'}, status=403)
            except:
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
    except:
        return JsonResponse({'error': 'Internal Server error'},status=500)
        
def admin_approve_event(request):
    try:
        user_role=get_user_role_from_jwt(request)
        if user_role != "ADMIN":
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        if request.method == 'POST':
            data = json.loads(request.body)
            approval_id = data.get('approval_id')
            action = data.get('action')  # 'approve' or 'reject'
            
            if not approval_id:
                return JsonResponse({'error': 'approval id is required'},status=400)
            if not action:
                return JsonResponse({'error': 'Action is required whether to approve or reject'}, status=400)
            
            approval_request = approval_collection.find_one({'_id': ObjectId(approval_id)})
            if approval_request and approval_request['action']=='post':
                try:
                    if action == 'approve':
                        result=event_collection.insert_one(
                            pending_events_collection.find_one({'_id': ObjectId(approval_request['event_id'])})
                        )
                        if result.inserted_id:
                            pending_events_collection.delete_one({'_id': ObjectId(approval_request['event_id'])})
                        else:
                            return JsonResponse({'error': 'Action could not be processed successfully, Try again'}, status=500)
                    else:
                        pending_events_collection.delete_one({'_id': ObjectId(approval_request['event_id'])})
                    approval_collection.update_one(
                        {'_id': ObjectId(approval_id)},
                        {'$set': {'approved': action == 'approve'}}
                    )
                    return JsonResponse({'message': 'Action processed successfully.'}, status=200)
                except:
                    return JsonResponse({'error': 'Action could not be processed successfully'}, status=500)
            
            elif approval_request and approval_request['action']=='put':
                try:
                    if action == 'approve':
                        filter={'_id': ObjectId(approval_request['event_id'])}
                        result = event_collection.replace_one(filter, pending_events_collection.find_one({'_id': ObjectId(approval_request['event_id'])}))
                        if result.modified_count>0:
                            pending_events_collection.delete_one({'_id': ObjectId(approval_request['event_id'])})
                        else:
                            return JsonResponse({'error': 'Action could not be processed successfully, Try again'}, status=500)
                    else:
                        pending_events_collection.delete_one({'_id': ObjectId(approval_request['event_id'])})
                    approval_collection.update_one(
                        {'_id': ObjectId(approval_id)},
                        {'$set': {'approved': action == 'approve'}}
                    )
                    return JsonResponse({'message': 'Action processed successfully.'}, status=200)
                except:
                    return JsonResponse({'error': 'Action could not be processed successfully'}, status=500)

            elif approval_request and approval_request['action']=='delete':
                try:
                    if action == 'approve':
                        result=event_collection.delete_one(
                            {'_id': ObjectId(approval_request['event_id'])}
                        )
                        if result.deleted_count>0:
                            pending_events_collection.delete_one({'_id': ObjectId(approval_request['event_id'])})
                        else:
                            return JsonResponse({'error': 'Action could not be processed successfully, Try again'}, status=500)
                    else:
                        pending_events_collection.delete_one({'_id': ObjectId(approval_request['event_id'])})
                    approval_collection.update_one(
                        {'_id': ObjectId(approval_id)},
                        {'$set': {'approved': action == 'approve'}}
                    )
                    return JsonResponse({'message': 'Action processed successfully.'}, status=200)
                except:
                    return JsonResponse({'error': 'Action could not be processed successfully'}, status=500)
            else:
                return JsonResponse({'error': 'Approval request not found.'}, status=404)
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
    except:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

def register_event(request):
    try:
        if request.method == 'POST':
            try:  
                user_role=get_user_role_from_jwt(request)
                if user_role!='USER': return JsonResponse({'error': 'Permission denied'}, status=403)
                data=json.loads(request.body)
                event_id=data['event_id']
                user_id=data['user_id']
                if not event_id or not user_id:
                    return JsonResponse({'error': 'Event ID and User ID are required'}, status=400)
                
                resultEvent = event_collection.update_one(
                            {'_id': ObjectId(event_id)},
                            {'$addToSet': {'attendees': user_id}}
                        )
                if resultEvent.modified_count>0:
                    resultUser = user_collection.update_one({'_id': ObjectId(user_id)},{'$addToSet': {'events':event_id}})
                else:
                    return JsonResponse({'error': 'Failed to register, Try again'}, status=500)
                
                if resultEvent.modified_count > 0 and resultUser.modified_count>0:
                    return JsonResponse({'message': 'User registered to event successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'Event not found or user already registered'}, status=404)
            except Exception as e:
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
    except:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    
    