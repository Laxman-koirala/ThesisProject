from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages


# Create your views here.
def Signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserCreationForm(request.POST)
            if fm.is_valid():
                username = fm.cleaned_data.get('username')
                messages.success(
                    request, f'Account created Successfully for {username}.')
                fm.save()
        else:
            fm = UserCreationForm()
        return render(request, 'Signup.html', {'form': fm})
    else:
        return HttpResponseRedirect('/postlist/')




# Login
def Login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                name = fm.cleaned_data['username']
                pw = fm.cleaned_data['password']
                user = authenticate(username=name, password=pw)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/postlist/')
        else:
            fm = AuthenticationForm()
        return render(request, 'Login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/postlist/')
# Logout
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# change password with older None
@login_required
def Change_Password(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/postlist/')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, 'Base.html', {'form': fm})

