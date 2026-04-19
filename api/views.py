from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Evenement, Predication, Temoignages, ProgrammeHebdo
from .serializers import (
    EvenementSerializer, 
    PredicationSerializer, 
    TemoignagesSerializer, 
    UserRegisterSerializer,
    ProgrammeHebdoSerializer
)

class RegisterUserView(generics.CreateAPIView):
    """
    Vue pour l'enregistrement d'un nouvel utilisateur (Inscription).
    Permet de créer un compte avec email et téléphone (stocké dans 'username').
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(APIView):
    """
    Vue permettant à un utilisateur connecté de récupérer ses propres informations.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retourne les détails de l'utilisateur actuellement authentifié par JWT.
        """
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff
        })

class EvenementViewSet(viewsets.ModelViewSet):
    """
    Gestion des événements.
    - Lecture publique autorisée.
    - Création/Modification réservée aux administrateurs via DjangoModelPermissions.
    """
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer

class PredicationViewSet(viewsets.ModelViewSet):
    """
    Gestion des prédications.
    - Lecture publique autorisée.
    - Création/Modification réservée aux administrateurs.
    """
    queryset = Predication.objects.all()
    serializer_class = PredicationSerializer

class TemoignagesViewSet(viewsets.ModelViewSet):
    """
    Gestion des témoignages avec modération automatique.
    """
    queryset = Temoignages.objects.all()
    serializer_class = TemoignagesSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Soumission publique d'un témoignage.
        Forcé à 'published=False' pour la modération.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(published=False)
            return Response(
                {
                    "message": "Votre témoignage a été reçu et est en attente de modération.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Filtrage des témoignages :
        - La liste publique affiche uniquement les témoignages publiés.
        - Les administrateurs peuvent tout voir.
        """
        if self.request.user.is_staff:
            return Temoignages.objects.all()

        if self.action == 'list':
            return Temoignages.objects.filter(published=True).order_by('-created_at')
        return Temoignages.objects.all()


class ProgrammeHebdoViewSet(viewsets.ModelViewSet):
    """
    Gestion du programme hebdomadaire.
    - Lecture publique.
    - Modification réservée aux administrateurs.
    """
    queryset = ProgrammeHebdo.objects.all()
    serializer_class = ProgrammeHebdoSerializer