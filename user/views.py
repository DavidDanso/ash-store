from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.decorators.csrf import csrf_protect

################################ register User views
@csrf_protect
def registerPage(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,  'user account created successful')
            login(request, user)
            return redirect('products')

    context = {'form': form}
    return render(request, 'user/register.html', context)

################################ login views
@csrf_protect
def loginPage(request):
    # 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,  'User not found')


        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            # user login success message
            messages.success(request,  'user login successful')
            return redirect('products')
        else:
            messages.error(request,  'Username or Password is incorrect')

    return render(request, 'user/login.html')

################################ logout views
def logoutPage(request):
    logout(request)
    return redirect('login')

#################################  user profle views
@login_required(login_url='login')
def profilePage(request):
    # user profile
    profile = request.user.profile
    # user profile form INSTANCE
    form = UserProfileForm(instance=profile)
    # user profile form
    form = UserProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        # create new folder message
        messages.success(request,  'profile updated successful')
        # change the 8000 to your port number 
        # if you're not using port 8000
    # else:
    #     profile.delete()
    #     # create new folder message
    #     messages.success(request, 'account delete successful')
    #     return redirect('home')

    context = {'form': form, 'profile': profile}
    return render(request, 'user/profile.html', context)




