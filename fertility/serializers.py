from rest_framework import serializers
from .models import Cycle, Fertility, Pregnancy

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'

class FertilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertility
        fields = '__all__'

class PregnancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregnancy
        fields = '__all__'
