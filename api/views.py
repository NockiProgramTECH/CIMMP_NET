from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator




from main.models import Evenement, LiveStream, Predication, ProgrammeHebdo, Temoignages

from .models import RendezVous, AppVersion, VerificationCode
from .serializers import (
    EvenementSerializer, 
    PredicationSerializer, 
    TemoignagesSerializer, 
    UserRegisterSerializer,
    ProgrammeHebdoSerializer,
    LiveStreamSerializer,
    RendezVousSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    RequestCodeSerializer,
    VerifyCodeSerializer
)
# @method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='post')
# class TokenObtainPairView(TokenObtainPairView):
#     pass



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RequestCodeView(APIView):
    """
    Génère et envoie un code de 6 chiffres par email pour l'inscription ou la réinitialisation.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RequestCodeSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            purpose = serializer.validated_data['purpose']
            
            # Destination de l'email
            email_dest = None
            
            if purpose == 'PASSWORD_RESET':
                # On cherche l'utilisateur par username (tél) ou email
                user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()
                if not user:
                    return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
                email_dest = user.email
                if not email_dest:
                    return Response({"error": "Aucun email associé à ce compte."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Pour l'inscription, l'identifiant doit être l'email
                if "@" not in identifier:
                    return Response({"error": "Veuillez fournir un email valide pour l'inscription."}, status=status.HTTP_400_BAD_REQUEST)
                email_dest = identifier

            # Génération du code
            code = VerificationCode.generate_code()
            VerificationCode.objects.create(
                identifier=identifier,
                code=code,
                purpose=purpose
            )
            
            # Envoi de l'email
            subject = "Votre code de vérification CIMPP"
            message = f"Votre code de vérification pour {purpose} est : {code}. Il expire dans 10 minutes."
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email_dest],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({"error": f"Erreur lors de l'envoi de l'email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                "message": f"Code de vérification envoyé à {email_dest}.",
                # "code": code # RETIRÉ POUR LA PRODUCTION
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    """
    Vérifie si le code de 6 chiffres est valide.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            code = serializer.validated_data['code']
            purpose = serializer.validated_data['purpose']
            
            verification = VerificationCode.objects.filter(
                identifier=identifier,
                code=code,
                purpose=purpose,
                is_used=False
            ).last()
            
            if verification and not verification.is_expired():
                return Response({"message": "Code valide."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Code invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(generics.CreateAPIView):
    """
    Vue pour l'enregistrement d'un nouvel utilisateur.
    Vérifie également le code de validation et connecte l'utilisateur.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        code = request.data.get('code')
        email = request.data.get('email')
        
        if not code or not email:
            return Response({"error": "L'email et le code de vérification sont requis."}, status=status.HTTP_400_BAD_REQUEST)
            
        verification = VerificationCode.objects.filter(
            identifier=email,
            code=code,
            purpose='REGISTER',
            is_used=False
        ).last()
        
        if not verification or verification.is_expired():
            return Response({"error": "Code de vérification invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Création de l'utilisateur
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Marquage du code comme utilisé
        verification.is_used = True
        verification.save()
        
        # Connexion automatique (Génération des tokens)
        tokens = get_tokens_for_user(user)
        
        return Response({
            "user": serializer.data,
            "tokens": tokens,
            "message": "Compte créé et connecté avec succès."
        }, status=status.HTTP_201_CREATED)

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
    queryset = Evenement.objects.all().order_by('-date')
    serializer_class = EvenementSerializer

class PredicationViewSet(viewsets.ModelViewSet):
    """
    Gestion des prédications (CRUD complet).
    - GET (list/retrieve) : Public.
    - POST, PUT, PATCH, DELETE : Admin uniquement.
    """
    queryset = Predication.objects.all().order_by('-date')
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
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.DjangoModelPermissionsOrAnonReadOnly()]

    def create(self, request, *args, **kwargs):
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
        if self.request.user.is_staff:
            return Temoignages.objects.all().order_by('-created_at')
        if self.action == 'list':
            return Temoignages.objects.filter(published=True).order_by('-created_at')
        return Temoignages.objects.all()

class RendezVousViewSet(viewsets.ModelViewSet):
    """
    Gestion des demandes de rendez-vous.
    - POST (create) : Reservé aux utilisateurs connectés.
    - GET (list/retrieve) : Reservé aux administrateurs.
    """
    queryset = RendezVous.objects.all().select_related('user')
    serializer_class = RendezVousSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
      

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
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
        if self.request.user.is_staff:
            return RendezVous.objects.all().select_related('user').order_by('-created_at')
        return RendezVous.objects.none()




class ProgrammeHebdoViewSet(viewsets.ModelViewSet):
    """
    Gestion du programme hebdomadaire (CRUD complet).
    - GET : Public.
    - POST, PUT, PATCH, DELETE : Admin.
    """
    queryset = ProgrammeHebdo.objects.all().order_by('ordre')
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
        if request.user.is_staff and request.query_params.get('all') == 'true':
            return super().list(request, *args, **kwargs)

        last_live = LiveStream.objects.filter(is_live=True).order_by('-updated_at').first()
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
    Demande de réinitialisation de mot de passe.
    Génère un code de 6 chiffres et l'envoie par email.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            try:
                # On cherche l'utilisateur (le username est le téléphone dans ce projet)
                user = User.objects.get(username=phone)
                email_dest = user.email
                
                if not email_dest:
                    return Response({"error": "Aucun email associé à ce compte pour l'envoi du code."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Génération du code
                code = VerificationCode.generate_code()
                VerificationCode.objects.create(
                    identifier=phone,
                    code=code,
                    purpose='PASSWORD_RESET'
                )
                
                # Envoi de l'email
                subject = "Réinitialisation de votre mot de passe CIMPP"
                message = f"Votre code de réinitialisation est : {code}. Il expire dans 10 minutes."
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email_dest],
                    fail_silently=False,
                )
                
                return Response({
                    "message": f"Un code de réinitialisation a été envoyé à {email_dest}.",
                    "phone": phone
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé avec ce numéro."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": f"Erreur d'envoi d'email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    """
    Réinitialisation effective du mot de passe et connexion automatique.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(username=phone)
                verification = VerificationCode.objects.filter(
                    identifier=phone,
                    code=code,
                    purpose='PASSWORD_RESET',
                    is_used=False
                ).last()
                
                if verification and not verification.is_expired():
                    user.set_password(new_password)
                    user.save()
                    
                    verification.is_used = True
                    verification.save()
                    
                    # Connexion automatique après reset
                    tokens = get_tokens_for_user(user)
                    
                    return Response({
                        "message": "Mot de passe réinitialisé avec succès.",
                        "tokens": tokens
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Code invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class HealthCheckView(APIView):
    """
    Endpoint de vérification de l'état de santé de l'API.
    Accessible sans authentification.
    Retourne le statut de l'API et la configuration minimale.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from django.db import connection
        db_ok = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            db_ok = False

        return Response({
            "status": "ok" if db_ok else "degraded",
            "database": "connected" if db_ok else "error",
            "version": "1.0.0",
        }, status=status.HTTP_200_OK if db_ok else status.HTTP_503_SERVICE_UNAVAILABLE)


class StatisticsView(APIView):
    """
    Endpoint public pour obtenir des statistiques globales
    (nombre de prédications, témoignages, événements).
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "predications": Predication.objects.count(),
            "evenements": Evenement.objects.count(),
            "temoignages_publics": Temoignages.objects.filter(published=True).count(),
        })


class PredicationSearchView(generics.ListAPIView):
    """
    Recherche avancée dans les prédications.
    Paramètres de requête :
    - `q` : recherche full-text dans titre, resume, contenu, predicateur
    - `theme` : filtre par thème exact
    - `date_from` : filtre par date minimale (YYYY-MM-DD)
    - `date_to` : filtre par date maximale (YYYY-MM-DD)
    """
    serializer_class = PredicationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Predication.objects.all().order_by('-date')
        q = self.request.query_params.get('q')
        theme = self.request.query_params.get('theme')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if q:
            queryset = queryset.filter(
                Q(titre__icontains=q) |
                Q(resume__icontains=q) |
                Q(contenu__icontains=q) |
                Q(predicateur__icontains=q)
            )
        if theme:
            queryset = queryset.filter(theme__iexact=theme)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset


from django.shortcuts import redirect
from django.http import Http404
from django.conf import settings
import boto3

def serve_media(request, path):
    """
    Génère une URL pré-signée Garage S3 et redirige le client directement vers elle.
    Django ne touche plus au fichier — chaque requête est traitée en ~2ms.
    Supporte des centaines d'utilisateurs simultanés sans bloquer de worker.
    """
    if not all([
        getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
        getattr(settings, 'AWS_ACCESS_KEY_ID', None),
        getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
    ]):
        raise Http404("Media storage not configured")

    s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        config=boto3.session.Config(signature_version='s3v4')
    )
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': path
            },
            ExpiresIn=3600
        )
        response = redirect(presigned_url)
        response['Cache-Control'] = 'public, max-age=3600'
        return response
    except Exception:
        raise Http404