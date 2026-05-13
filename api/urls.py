from django.urls import path, include
from rest_framework import routers 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    EvenementViewSet, 
    PredicationViewSet, 
    TemoignagesViewSet,
    RegisterUserView,
    UserProfileView,
    ProgrammeHebdoViewSet,
    LiveStreamViewSet,
    RendezVousViewSet,
    AppVersionAPIView,
    ForgotPasswordView,
    ResetPasswordView
)

# Routeur pour les ModelViewSets standards
router = routers.DefaultRouter()
router.register(r'evenements', EvenementViewSet)
router.register(r'predications', PredicationViewSet)
router.register(r'temoignages', TemoignagesViewSet)
router.register(r'programmes-hebdo', ProgrammeHebdoViewSet)
router.register(r'rdv',RendezVousViewSet)
router.register(r'live', LiveStreamViewSet, basename='live')

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Routes du routeur (CRUD Evenements, Predications, Temoignages)
    path('', include(router.urls)),
    
    # --- Documentation API (OpenAPI/Swagger) ---
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # UI pour Swagger
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # UI pour Redoc (alternative)
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # --- Authentification et Comptes ---
    
    # Inscription d'un nouvel utilisateur
    path('auth/register/', RegisterUserView.as_view(), name='auth_register'),
    
    # Connexion : Obtention du jeton JWT (Email/Téléphone + Password)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Rafraîchissement du jeton
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profil utilisateur connecté
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),

    # Version de l'application
    path('version-app/', AppVersionAPIView.as_view(), name='version-app'),

    # --- Réinitialisation de mot de passe ---
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]
