from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscription, name='inscription'),
    # Ajoutez d'autres configurations d'URL au besoin
]
