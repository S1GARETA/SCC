from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import CoreSerializer, BoostSerializer
from .models import Core, Boost
from .forms import UserForm


@login_required
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)
    return render(request, 'credits/index.html', {'core': core, 'boosts': boosts})


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)

    return Response({
        'core': CoreSerializer(core).data,
    })


@api_view(['POST'])
def update_coins(request):
    coins = request.data['coins']
    core = Core.objects.get(user=request.user)
    core.update_coins(coins)

    return Response({'core': CoreSerializer(core).data})


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = self.queryset.filter(core=core)
        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins']
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(coins)
        if not is_levelup:
            return Response({"error": "Не хватает денег"})

        old_boost_values, new_boost_values = is_levelup

        return Response({
            "old_boost_values": self.serializer_class(old_boost_values).data,
            "new_boost_values": self.serializer_class(new_boost_values).data,
        })


def registration(request):
    if request.method == 'POST':
        if request.POST.get('password_confirm') == None:
            print('Вход')
            user_form = UserForm()
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
            if user:
                login(request, user)
                return redirect('main')
            return render(request, 'credits/registration.html', {'user_form': user_form, 'invalid': True})
        else:
            print('Регистрация')
            user_form = UserForm(request.POST)  # регистрация
            if user_form.is_valid():
                user = user_form.save()
                core = Core(user=user)
                core.save()
                login(request, user)
                Boost.objects.create(core=core, price=10, power=1, name='miska_ris', type=0)
                Boost.objects.create(core=core, price=100, power=1, name='help_old', type=1)
                Boost.objects.create(core=core, price=250, power=1, name='charity', type=1)
                return redirect('main')
            return render(request, 'credits/registration.html', {'user_form': user_form})

    user_form = UserForm()
    return render(request, 'credits/registration.html', {'user_form': user_form})


@login_required
def guide(request):
    return render(request, 'credits/tytorial.html')


@login_required
def soon(request):
    return render(request, 'credits/soon.html')


def user_logout(request):
    logout(request)
    return redirect('login')
