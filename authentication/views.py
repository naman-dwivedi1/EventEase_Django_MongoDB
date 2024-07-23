from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password,check_password
from .models import user_collection,User
import re
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
import json

load_dotenv()

regexEmail=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

regexPassword=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'

def generate_jwt_token(user):
    payload = {
        'user_id': str(user['_id']),
        'role':user['role'],
        'exp': datetime.utcnow() + timedelta(hours=6),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, f'{os.getenv('SECRET_KEY')}', algorithm=f'{os.getenv('SECRET_ALGORITHM')}')
    return token

def signup(request):
    try:
        if request.method == "POST":
            data=json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            
            if username is None: return JsonResponse({'error': "Username not provided"}, status=400)
            if email is None: return JsonResponse({'error': "Email not provided"}, status=400)
            if password is None: return JsonResponse({'error': "Password not provided"}, status=400)

            if user_collection.find_one({"email": email}):
                return JsonResponse({'error': 'Email already exists'}, status=400)

            if(re.fullmatch(regexEmail,email)==None): return JsonResponse({'error': 'Please provide email in correct format'}, status=400)
            # if(re.fullmatch(regexPassword,password)==None): return JsonResponse({'error': 'Please provide a strong password'}, status=400)
            hashed_password = make_password(password)
            role='USER'
            new_user = User(email=email, username=username, password=hashed_password,role=role)
            result = user_collection.insert_one(new_user.to_dict())
            if result.inserted_id:
                return JsonResponse({'message': 'User created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Failed to create user'}, status=500)
        else:
            return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
    except:
        return JsonResponse({'error': 'Internal Server Error, Please try again'}, status=500)

def signin(request):
    try:
        if request.method == 'POST':
            data=json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            if email is None: return JsonResponse({'error': "Email not provided"}, status=400)
            if password is None: return JsonResponse({'error': "Password not provided"}, status=400)

            user_data = user_collection.find_one({"email": email})
            if user_data and check_password(password, user_data['password']):
                token = generate_jwt_token(user_data)
                return JsonResponse({'token': token}, status=200)
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
    except:
        return JsonResponse({'error':"Internal Server Error, Please try again"},status=500)