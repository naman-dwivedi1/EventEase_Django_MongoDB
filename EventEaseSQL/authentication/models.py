from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, default='ADMIN')

    def set_password(self, raw_password):
        """Hash the password before saving it."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Check if the given password is correct."""
        return check_password(raw_password, self.password)
    
    @classmethod
    def create_user(cls, email, username, password,role):
        user = cls(email=email, username=username,role=role)
        user.set_password(password)
        user.save()
        return user

    # def __str__(self):
    #     return self.username