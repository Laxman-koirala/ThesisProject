from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'Home.html')

def Login(request):
    return render(request, 'Login.html')