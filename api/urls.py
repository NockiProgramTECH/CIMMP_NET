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
    ProgrammeHebdoViewSet
)

# Routeur pour les ModelViewSets standards
router = routers.DefaultRouter()
router.register(r'evenements', EvenementViewSet)
router.register(r'predications', PredicationViewSet)
router.register(r'temoignages', TemoignagesViewSet)
router.register(r'programmes-hebdo', ProgrammeHebdoViewSet)

urlpatterns = [
    # Routes du routeur (CRUD Evenements, Predications, Temoignages)
    path('', include(router.urls)),

    # --- Authentification et Comptes ---

    # Inscription d'un nouvel utilisateur
    path('auth/register/', RegisterUserView.as_view(), name='auth_register'),

    # Connexion : Obtention du jeton JWT (Email/Téléphone + Password)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Rafraîchissement du jeton
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profil utilisateur connecté
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),
]