from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, postData):    
        errors = {}
        if len(postData['firstName']) < 2:
            errors["firstName"] = "First Name must be at least 2 characters"
        if len(postData['lastName']) < 2:
            errors["lastName"] = "Last Name must be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"]  = "Password description should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords must match!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        return errors

# Create your models here.
class User(models.Model):
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


