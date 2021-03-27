from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from .models import User, Wall_Message, Comment


def log_and_reg(request):
    return render(request, "log_and_reg.html")

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                messages.success(request, "Successfully logged in!")
                return redirect('/wall')
            messages.error(request, "Incorrect email/password combination")
        else:
            messages.error(request, "Email not found in DB.")
    return redirect("/")

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                firstName=request.POST['firstName'],
                lastName=request.POST['lastName'],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['user_id'] = user.id
            messages.success(request, "Successfully registered!")
            return redirect("/wall")
    return redirect("/")

def wall(request):
    if not 'user_id' in request.session:
        return redirect("/")
    context = {
            "user": User.objects.get(id=request.session['user_id']),
            "wall_messages": Wall_Message.objects.all()

    }
    return render(request, "wall.html", context)


def post_message(request):
    if request.method == 'POST':
        errors = Wall_Message.objects.message_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:    
            Wall_Message.objects.create(message=request.POST['message'], poster=User.objects.get(id=request.session['user_id']))
    return redirect("/wall")


def post_comment(request, wall_message_id):
    if request.method == 'POST':
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:    
            Comment.objects.create(
                comment = request.POST['comment'], 
                poster = User.objects.get(id=request.session['user_id']),
                wall_message = Wall_Message.objects.get(id=wall_message_id)
            )            
    return redirect("/wall")

def delete_message(request, wall_message_id):
    if request.method == "POST":
        wall_message = Wall_Message.objects.get(id=wall_message_id)
        wall_message.delete()
    return redirect("/wall")


#def delete_comment(request, wall_message_id):

        
def logout(request):
    request.session.flush()
    return redirect("/")