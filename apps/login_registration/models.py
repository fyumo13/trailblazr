from django.db import models
from datetime import datetime
import bcrypt
import re 

# regex to test if given name contains letters only and is at least 2 letters long
name_regex = re.compile(r'[A-Za-z]{2,}')
# regex to test if given email is valid
email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-z]*$')
# regex to test if given password is at least 8 characters long, contains 1 lowercase alphabetical characters, contains 1 uppercase alphabetical
# character, contains at least 1 numeric character, and contains at least 1 special character
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')
# regex to test if given date is in valid MM/DD/YYYY format
date_regex = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}')

class UserManager(models.Manager):
    def register(self, postData):
        # runs validation test
        errors = self.validate(postData)
        # creates a hashed password and stores user info into a new User object
        if not errors:
            hashed_password = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed_password.decode('utf-8'),
            )
            user.save()
            return user
        else:
            return errors

    # searches for Users matching the given email and tests if the given password matches the stored password
    def login(self, postData):
        user = User.objects.filter(email=postData['email'])
        if not user:
            return False
        if bcrypt.hashpw(postData['password'].encode('utf-8'), user[0].password.encode('utf-8')) != user[0].password.encode('utf-8'):
            return False 
        else:
            return user[0]

    # deletes the session attached to the given user ID
    def logout(self, session):
        del session
        return True

    # tests whether the given user first name, last name, email, and password are all valid
    def validate(self, postData):
        errors = []
        try:
            user = User.objects.get(email=postData['email'])
            errors.append('User email already exists! Please log in.')
        except:
            if not re.match(name_regex, postData['first_name']):
                errors.append('First name must be more than 2 characters!')
            if not re.match(name_regex, postData['last_name']):
                errors.append('Last name must be more than 2 characters!')
            if not re.match(email_regex, postData['email']):
                errors.append('Email address is invalid!')
            if not re.match(password_regex, postData['password']):
                errors.append('Password is invalid!')
            elif postData['password'] != postData['confirm_password']:
                errors.append('Passwords do not match!')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)