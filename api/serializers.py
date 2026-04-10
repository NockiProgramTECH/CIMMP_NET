from dataclasses import fields
from pyexpat import model

from fpdf import Template
from rest_framework import serializers
from main.models import Evenement,Predication,Temoignages

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model =Evenement
        fields = '__all__'
    


class PredicationSerializer(serializers.ModelSerializer):
      class Meta:
        model =Predication
        fields = '__all__'


class TemoignagesSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model =Temoignages
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 
            'phone', 'subjet', 'temoignage', 'created_at', 'published'
        ]
        read_only_fields = ['created_at']
    
    def create(self,validated_data):
        return Temoignages.objects.create(**validated_data)
    
