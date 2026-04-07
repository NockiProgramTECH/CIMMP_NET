from django.urls import path

from . import views

app_name ="main"


urlpatterns = [
    path('',views.index,name="index"),
    path('submit-temoignage/', views.submit_temoignage, name='submit_temoignage'),
    path('predications/', views.predications_list, name='predications_list'),
    path('predications/<str:slug>/', views.predication_detail, name='predication_detail'),


]
