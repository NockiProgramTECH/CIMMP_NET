from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,permissions,status
from rest_framework.response import Response

from main.models import Evenement,Predication,Temoignages
from .serializers import EvenementSerializer,PredicationSerializer,TemoignagesSerializer


class EvenementViewSet(viewsets.ModelViewSet):
    queryset =Evenement.objects.all()
    serializer_class=EvenementSerializer




class PredicationViewSet(viewsets.ModelViewSet):
    queryset =Predication.objects.all()
    serializer_class=PredicationSerializer




class TemoignagesViewSet(viewsets.ModelViewSet):
    queryset = Temoignages.objects.all()
    serializer_class = TemoignagesSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Utilise directement 'request.data' au lieu de 'self.request.data'
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # On force le statut non publié pour la modération
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
        # Pour la liste publique, on ne montre que ce qui est validé
        if self.action == 'list':
            return Temoignages.objects.filter(published=True).order_by('-created_at')
        # Pour le reste (détails, etc.), on autorise l'accès complet
        return Temoignages.objects.all()