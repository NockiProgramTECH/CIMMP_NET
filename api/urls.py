from django.urls import path

from rest_framework import routers 


from .views import EvenementViewSet,PredicationViewSet,TemoignagesViewSet


router =routers.DefaultRouter()
router.register(r'evenements',EvenementViewSet)
router.register(r'predications',PredicationViewSet)
router.register(r'temoignages',TemoignagesViewSet)

urlpatterns =router.urls