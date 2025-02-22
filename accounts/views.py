from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.handlers.modwsgi import check_password
from django.shortcuts import render, redirect

from accounts.models import CustomUser


# Create your views here.
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout successful')
        return redirect("/accounts/login")
    else:
        return redirect("/dashboard/")



def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        # use check_password to check if the password is correct
        user = CustomUser.objects.get(email=email)
        if not user.check_password(password):
            user = None

        if user is not None:
            messages.success(request, 'Login successful')
            login(request, user)
            return redirect("/dashboard/")
        else:
            messages.error(request, 'Email or password is incorrect')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')
