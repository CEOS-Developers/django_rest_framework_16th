from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from todoapp.models import Profile


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            nickname = request.POST["nickname"]
            message = request.POST["message"]
            profile = Profile(user=user, nickname=nickname, message=message)
            profile.save()
            auth.login(request,user)
            return redirect('account:home')
    return render(request, 'account/signup.html')