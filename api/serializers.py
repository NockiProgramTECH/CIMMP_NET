from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Evenement, Predication, Temoignages, ProgrammeHebdo, LiveStream
from .models import RendezVous


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création d'un compte utilisateur (Inscription).
    Le 'username' peut être utilisé comme numéro de téléphone.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        """
        Crée un utilisateur avec un mot de passe haché.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class EvenementSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Evenement.
    """
    class Meta:
        model = Evenement
        fields = '__all__'


class PredicationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Predication.
    """
    class Meta:
        model = Predication
        fields = '__all__'


class TemoignagesSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Temoignages avec support de la modération.
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Temoignages
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 
            'phone', 'subjet', 'temoignage', 'created_at', 'published'
        ]
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        """
        Crée un témoignage. Par défaut, published est False via la vue.
        """
        return Temoignages.objects.create(**validated_data)


class ProgrammeHebdoSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle ProgrammeHebdo.
    """
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = ProgrammeHebdo
        fields = '__all__'

class LiveStreamSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle LiveStream.
    """
    class Meta:
        model = LiveStream
        fields = '__all__'



class RendezVousSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = RendezVous
        fields = ['id', 'user','first_name','last_name', 'date_rdv', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(help_text="Le numéro de téléphone (username) de l'utilisateur")


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(help_text="Le numéro de téléphone (username) de l'utilisateur")
    token = serializers.CharField(help_text="Le jeton reçu pour la réinitialisation")
    new_password = serializers.CharField(min_length=6, write_only=True, help_text="Le nouveau mot de passe")

