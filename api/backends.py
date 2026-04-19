from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class PhoneOrEmailBackend(ModelBackend):
    """
    Backend d'authentification personnalisé permettant de se connecter
    via l'adresse email ou le nom d'utilisateur (qui peut être un numéro de téléphone).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            # Recherche par email ou username (téléphone)
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Si plusieurs utilisateurs ont le même email (cas rare si email unique)
            return User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
