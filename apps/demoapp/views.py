from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.encoding import smart_text
import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'demoapp/loginreg.html')

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        name = request.POST['name']
        regErrors = Users.objects.validation(email, password, conf_password, name)
        print(regErrors)
        if regErrors:
            for error in regErrors:
                messages.error(request, smart_text(error))
            return render(request, 'demoapp/loginreg.html')
        else:
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = Users.objects.create(email=email, pw_hash=pw_hash, name=name)
            messages.success(request, "You have registered successfully")
            user.save()
            request.session['logged_user'] = user.id
            return redirect('/')

def loginForm(request):
    return render(request, 'demoapp/login.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        currentUser = Users.objects.loginValid(email, password)
        if type(currentUser) == list:
            for err in currentUser:
                messages.error(request, smart_text(err))
            return render(request, 'demoapp/loginForm')
        else:
            request.session['logged_user'] = currentUser.id
            return redirect('/all_quotes')

def quotes(request):
    user = Users.objects.filter(id=request.session['logged_user'])
    print(user)
    return render(request, 'demoapp/quotes.html')

def guestQuotes(request):
    return render(request, 'demoapp/guestquotes.html')

def log_out(request):
    logout(request)
    return redirect('/')
