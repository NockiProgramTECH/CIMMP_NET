from django.urls import path

from . import views

app_name ="main"


urlpatterns = [
    path('',views.index,name="index"),
    path('submit-temoignage/', views.submit_temoignage, name='submit_temoignage'),
    path('predications/<str:slug>/',views.predication_detail,name="predications"),


]
