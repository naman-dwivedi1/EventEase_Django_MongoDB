from db_connection import db

user_collection=db['users']

class User:
    def __init__(self, email, username, password, role, events=None):
        self.email = email
        self.username = username
        self.password = password
        self.events = events if events is not None else []
        self.role=role

    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "events":self.events,
            "role":self.role
        }