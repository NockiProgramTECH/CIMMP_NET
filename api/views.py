from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import RendezVous
from main.models import Evenement, Predication, Temoignages, ProgrammeHebdo, LiveStream
from .serializers import (
    EvenementSerializer, 
    PredicationSerializer, 
    TemoignagesSerializer, 
    UserRegisterSerializer,
    ProgrammeHebdoSerializer,
    LiveStreamSerializer,
    RendezVousSerializer
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
    Gestion des événements (CRUD complet).
    - GET (list/retrieve) : Public (AnonReadOnly).
    - POST, PUT, PATCH, DELETE : Admin uniquement (DjangoModelPermissions).
    """
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    # Utilise la permission par défaut : DjangoModelPermissionsOrAnonReadOnly

class PredicationViewSet(viewsets.ModelViewSet):
    """
    Gestion des prédications (CRUD complet).
    - GET (list/retrieve) : Public.
    - POST, PUT, PATCH, DELETE : Admin uniquement.
    """
    queryset = Predication.objects.all()
    serializer_class = PredicationSerializer

class TemoignagesViewSet(viewsets.ModelViewSet):
    """
    Gestion des témoignages (CRUD complet).
    - POST (create) : Public.
    - GET (list) : Public (uniquement les publiés) ou Admin (tous).
    - PUT, PATCH, DELETE : Admin uniquement.
    """
    queryset = Temoignages.objects.all()
    serializer_class = TemoignagesSerializer

    def get_permissions(self):
        """
        Définit les permissions selon l'action.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.DjangoModelPermissionsOrAnonReadOnly()]

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

class RendezVousViewSet(viewsets.ModelViewSet):
    """
    Gestion des demandes de rendez-vous.
    - POST (create) : Reservé aux utilisateurs connectés.
    - GET (list/retrieve) : Reservé aux administrateurs.
    """
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer

    def get_permissions(self):
        """
        Définit les permissions selon l'action.
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        """
        Associe automatiquement le rendez-vous à l'utilisateur connecté.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Surcharge de la création pour retourner un message personnalisé.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Votre demande de rendez-vous a été bien reçue et est en attente de confirmation.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Seuls les administrateurs voient la liste complète, triée par date de création.
        """
        if self.request.user.is_staff:
            return RendezVous.objects.all().order_by('-created_at')
        return RendezVous.objects.none()




class ProgrammeHebdoViewSet(viewsets.ModelViewSet):
    """
    Gestion du programme hebdomadaire (CRUD complet).
    - GET : Public.
    - POST, PUT, PATCH, DELETE : Admin.
    """
    queryset = ProgrammeHebdo.objects.all()
    serializer_class = ProgrammeHebdoSerializer

class LiveStreamViewSet(viewsets.ModelViewSet):
    """
    Gestion du lien direct (Live Stream) (CRUD complet).
    - GET : Retourne le direct actuel (list personnalisé) ou un spécifique (retrieve).
    - POST, PUT, PATCH, DELETE : Admin.
    """
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer

    def list(self, request, *args, **kwargs):
        """
        Cas particulier pour le Frontend : retourne le dernier direct actif.
        Si l'utilisateur est admin et veut la liste réelle, il peut utiliser le paramètre ?all=true
        """
        if request.user.is_staff and request.query_params.get('all') == 'true':
            return super().list(request, *args, **kwargs)
            
        last_live = LiveStream.objects.last()
        if last_live:
            serializer = self.get_serializer(last_live)
            return Response(serializer.data)
        return Response({"message": "Aucun direct configuré"}, status=status.HTTP_404_NOT_FOUND)
