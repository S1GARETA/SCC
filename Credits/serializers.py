from rest_framework.serializers import ModelSerializer
from .models import Core, Boost


class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'coins_per_second']


class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'