import jwt
import os
from dotenv import load_dotenv

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