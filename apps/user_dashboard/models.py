from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def name_invalid(self, name):
        if not len(name) < 2 and re.search(r'^[a-zA-Z]+$', name):
            return False
        else:
            return True
    def email_invalid(self, email):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if email_regex.match(email):
            return False
        else:
            return True
    def password_invalid(self, password):
        if len(password) < 8:
            return True
        else:
            return False
    def password_not_match(self, password, confirm_password):
        if password == confirm_password:
            return False
        else:
            return True

    def reg_validator(self, first_name, last_name, email, password, confirm_password):
        errors = []
        if self.name_invalid(first_name):
            errors.append("First name must be more than two characters and only letters")
        if self.name_invalid(last_name):
            errors.append("Last name must be more than two characters and only letters")
        if self.email_invalid(email):
            errors.append("Invalid email")
        if self.password_invalid(password):
            errors.append("Password must be 8 characters or more")
        if self.password_not_match(password, confirm_password):
            errors.append("Passwords must match")
        return errors
## returns an object with either {errors: list of errors}, or {user: user object}
    def add_user(self, first_name, last_name, email, password, confirm_password):
        errors = self.reg_validator(first_name, last_name, email, password, confirm_password)
        if errors:
            return {'errors': errors}
        else:
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            if not User.objects.all():
                user_level = 9
            else:
                user_level = 1
            try:
                user = User(first_name=first_name, last_name=last_name, email=email, hash_pw=hash_pw, user_level=user_level)
                user.save()
                return {"user": user}
            except:
                return {"errors": ["Email already registered"]}
## returns an object with either {errors: list of errors}, or {user: user object}
    def login(self, email, password):
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode(), user.hash_pw.encode()) == user.hash_pw:
                return {"user": user}
            else:
                return {"errors": ["Invalid email or password"]}
        except:
            return {"errors": ["Invalid email or password"]}

    def update_name(self, email, first_name, last_name, id, user_level=1):
        errors = []
        if self.email_invalid(email):
            errors.append("Invalid email")
        if self.name_invalid(first_name):
            errors.append("First name must be more than two characters and only letters")
        if self.name_invalid(last_name):
            errors.append("Last name must be more than two characters and only letters")
        if errors:
            return {'errors': errors}
        user = User.objects.get(id=id)
        user.first_name = first_name
        user.last_name = last_name
        if user.email == email:
            pass
        elif User.objects.filter(email=email):
            return {"errors": ["Email already registered"]}
        user.email = email
        if user_level > 0:
            user.user_level = user_level
        user.save()
        return {"user": user}

    def update_password(self, password, confirm_password, id):
        errors = []
        if self.password_invalid(password):
            errors.append("Password must be 8 characters or more")
        if self.password_not_match(password, confirm_password):
            errors.append("Passwords must match")
        if errors:
            return {'errors': errors}
        user = User.objects.get(id=id)
        user.hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return {"user": user}

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_level = models.IntegerField()
    description = models.TextField(max_length=100, default="")
    email = models.CharField(max_length=255, unique=True)
    hash_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    content = models.TextField(max_length = 1000)
    sender = models.ForeignKey(User, related_name="sent_messages", default=None)
    receiver = models.ForeignKey(User, related_name="received_messages", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField(max_length = 1000)
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name="message_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
