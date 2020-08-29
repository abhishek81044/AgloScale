from django.shortcuts import render
from account.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    return render(request,'account/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_admin = True
            user.is_superuser = True
            user.is_staff = True
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'account/signup.html',
                          {'user_form':user_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                users = [str(user) for user in User.objects.all()]
                return render(request, 'account/profile.html', {'users':users})
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'account/login.html', {})

def delete_user(request):
    if request.method == 'POST':
        selected_user = request.POST.get('drop')
        print("Selected User : ",selected_user)

        User.objects.filter(username=selected_user).delete()
        print("User Delete")

        users = [str(user) for user in User.objects.all()]
        return render(request, 'account/profile.html', {'users':users})
    else:
        return render(request, 'account/login.html', {})
