from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .models import *



def index(request):
    events =Evenement.objects.all()
    #filtrer les 3 dernier predications
    predication =Predication.objects.filter().order_by('-created_at')[:3]
    temoignages =Temoignages.objects.filter(published=True).order_by('-created_at')[:3]
    context ={
        'events':events,
        'predications':predication,
        'temoignages':temoignages
    }

    return render(request,"main/index_2.html",context)

def predications_list(request):
    predications = Predication.objects.all().order_by('-date')[:20]
    context = {
        'predications': predications
    }
    return render(request, "main/predications.html", context)


def predication_detail(request,slug):
    pre_detail =get_object_or_404(Predication,slug=slug)
  
    context = {
        'pre_detail': pre_detail,

        'related_predications': Predication.objects.exclude(id=pre_detail.id).order_by('-date')[:5]
    }
    
    return render(request,"main/predications_details.html",context)

#recevoir les requette ajax (js --->Django)

@csrf_exempt  # ⚠️ à supprimer quand CSRF est actif dans le front-end
def submit_temoignage(request):
    """Reçoit un témoignage via AJAX JSON POST et stocke en base."""

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))

        prenom = (data.get('prenom') or '').strip()
        nom = (data.get('nom') or '').strip()
        telephone = (data.get('telephone') or '').strip()
        cat_temoin = (data.get('categorie') or '').strip()
        message = (data.get('message') or '').strip()

        # Validation côté serveur
        if not all([prenom, nom, telephone, cat_temoin, message]):
            return JsonResponse({'success': False, 'error': 'Champs manquants'}, status=400)

        if len(message) < 20:
            return JsonResponse({'success': False, 'error': 'Message trop court (min 20 caractères)'}, status=400)

        # Enregistrement en base de données
        temoignage_obj = Temoignages.objects.create(
            first_name=prenom,
            last_name=nom,
            phone=telephone,
            subjet=cat_temoin,
            temoignage=message
        )

        return JsonResponse({'success': True, 'id': temoignage_obj.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erreur serveur: {str(e)}'}, status=500)






