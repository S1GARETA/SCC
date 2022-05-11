from django.shortcuts import render
from .models import TestDBUser


def index(request):
    return render(request, 'credits/index.html')

def login(request):
    return render(request, 'credits/registration.html')

def test(request):
    tests = TestDBUser.objects.all()
    return render(request, 'credits/testDB.html', {'tests': tests, 'user': request.user})