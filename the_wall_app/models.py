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

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors= {}
        if len(postData['message']) < 1:
            errors["message"] = "Wall Message must be at least 1 character"
        return errors

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors= {}
        if len(postData['comment']) < 1:
            errors["comment"] = "Comment must be at least 1 character"
        return errors

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="wall_message_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()


