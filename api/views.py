from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator

from api.models import RendezVous, AppVersion
from main.models import Evenement, Predication, Temoignages, ProgrammeHebdo, LiveStream
from .serializers import (
    EvenementSerializer, 
    PredicationSerializer, 
    TemoignagesSerializer, 
    UserRegisterSerializer,
    ProgrammeHebdoSerializer,
    LiveStreamSerializer,
    RendezVousSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
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

class AppVersionAPIView(APIView):
    """
    Vue pour vérifier la dernière version de l'application.
    Priorise l'URL externe si elle est définie.
    """
    permission_classes = [] 

    def get(self, request, *args, **kwargs):
        latest_version = AppVersion.objects.filter(is_active=True).order_by('-created_at').first()
        
        if latest_version:
            apk_url = None
            if latest_version.external_url:
                apk_url = latest_version.external_url
            elif latest_version.apk_file:
                apk_url = request.build_absolute_uri(latest_version.apk_file.url)
            
            if apk_url:
                return Response({
                    "version": latest_version.version,
                    "url": apk_url,
                    "force_update": latest_version.force_update
                })
            
        return Response({"detail": "Aucune mise à jour disponible."}, status=404)

class ForgotPasswordView(APIView):
    """
    Demande de réinitialisation de mot de passe via le numéro de téléphone.
    Génère un jeton qui devra être utilisé pour changer le mot de passe.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            try:
                user = User.objects.get(username=phone)
                # Génération du jeton
                token = default_token_generator.make_token(user)
                
                # Dans une application réelle, on enverrait ce token par SMS.
                # Ici, pour le test, on le retourne dans la réponse ou on log.
                return Response({
                    "message": "Un jeton de réinitialisation a été généré.",
                    "token": token,  # À retirer en production une fois l'envoi SMS configuré
                    "phone": phone
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # Pour des raisons de sécurité, on peut aussi retourner 200 même si l'utilisateur n'existe pas
                return Response({"error": "Utilisateur non trouvé avec ce numéro."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    """
    Réinitialisation effective du mot de passe en utilisant le jeton.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(username=phone)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Jeton invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# À ajouter à la fin de api/views.py

from django.http import StreamingHttpResponse, Http404
import boto3

def serve_media(request, path):
    s3 = boto3.client(
        's3',
        endpoint_url='http://192.168.1.69:3900',
        aws_access_key_id='GK36585bb667d2b9df10a292c8',
        aws_secret_access_key='bd07599fd632c59a047487893473fc56772980fa61f0b79d5eda15c0955193df',
        region_name='garage',
        config=boto3.session.Config(signature_version='s3v4')
    )
    try:
        obj = s3.get_object(Bucket='video', Key=path)
        content_type = obj.get('ContentType', 'video/mp4')
        file_size = obj['ContentLength']

        # Streaming par chunks de 8MB
        def file_iterator(body, chunk_size=8 * 1024 * 1024):
            while True:
                chunk = body.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        response = StreamingHttpResponse(
            file_iterator(obj['Body']),
            content_type=content_type
        )
        response['Content-Length'] = file_size
        response['Cache-Control'] = 'public, max-age=86400'
        response['Accept-Ranges'] = 'bytes'
        return response

    except Exception:
        raise Http404