from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from .models import User

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
                return redirect('/success')
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
            return redirect("/success")
    return redirect("/")

def success(request):
    if not 'user_id' in request.session:
        return redirect("/")
    context = {
            "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect("/")