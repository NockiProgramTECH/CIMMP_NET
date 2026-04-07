# TODO: Convertir predications.html en template Django complet avec suppression des doublons

## Plan approuvé - Étapes à compléter:

### 1. [x] Ajouter URLs (main/urls.py) ✅
   - path('predications/', views.predications_list, name='predications_list')
   - path('predications/<slug:slug>/', views.predication_detail, name='predication_detail') ✅

### 2. [x] Créer/Modifier views (main/views.py) ✅
   - def predications_list ✅
   - predication_detail avec related_predications ✅

### 3. [ ] Modifier template (templates/main/predications.html)

### 4. [ ] Tester

### 5. [ ] DB si vide

### 3. [ ] Modifier template (templates/main/predications.html)
   - Supprimer bloc featured-layout dupliqué
   - Ajouter {% for %} pour grille dynamique avec liens detail
   - Conditionnel detail/list via if pre_detail
   - JSON pour modal JS dynamique
   - Supprimer données statiques hardcoded

### 4. [ ] Tester
   - python manage.py runserver
   - Vérifier /predications/ (liste)
   - Vérifier /predications/un-slug/ (détail)
   - Vérifier suppression doublons, liens fonctionnent

### 5. [ ] DB si vide
   - python manage.py shell → créer quelques Predication via admin ou shell

**Prochaine étape: urls.py**
