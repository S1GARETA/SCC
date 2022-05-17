from django.shortcuts import render
from .models import TestDBUser


def index(request):
    print(str(request.user))
    if (str(request.user) != 'AnonymousUser'):
        return render(request, 'credits/index.html', {'username': request.user})
    else:
        return login(request)

def login(request):
    return render(request, 'credits/registration.html')

def guide(request):
    return render(request, 'credits/tytorial.html', {'username': request.user})

def soon(request):
    return render(request, 'credits/soon.html')



def test(request):
    # tests = TestDBUser.objects.all()
    # , {'tests': tests, 'user': request.user}
    return render(request, 'credits/testDB.html')