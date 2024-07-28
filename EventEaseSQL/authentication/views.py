from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login
from .models import User
import json
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=6),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm=os.getenv('SECRET_ALGORITHM'))
    return token

def signup(request):
    if request.method == "POST":
        # try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            
            if not email or not username or not password:
                return JsonResponse({'error': 'Email, username, and password are required'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            user = User(email=email, username=username)
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        # except Exception as e:
        #     return JsonResponse({'error': 'Internal Server Error, Please try again'}, status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

def signin(request):
    if request.method == 'POST':
        # try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)
            
            try:
                user = User.objects.get(email=email)
            except:
                return JsonResponse({'error': 'User with this email does not exists'}, status=400) 

            if user and user.check_password(password):
                token = generate_jwt_token(user)
                return JsonResponse({'token': token}, status=200)
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        # except Exception as e:
        #     return JsonResponse({'error': 'Internal Server Error, Please try again'}, status=500)
    else:
        return HttpResponseNotAllowed(['POST'])
