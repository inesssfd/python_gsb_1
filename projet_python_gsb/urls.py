# -*- coding: utf-8 -*-

"""
URL configuration for projet_python_gsb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from projetgsbpython.views import inscription
from django.urls import include
from projetgsbpython.views import inscription, connexion, tableau_de_bord, create_rapport, modifier_rapport,supprimer_rapport,index,profil_visiteur

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tableau_de_bord/<int:visiteur_id>/', tableau_de_bord, name='tableau_de_bord'),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('create_rapport/<int:visiteur_id>/',create_rapport, name='create_rapport'),
    path('modifier_rapport/<int:rapport_id>/',modifier_rapport, name='modifier_rapport'),
    path('supprimer_rapport/<int:rapport_id>/', supprimer_rapport, name='supprimer_rapport'),
    path('index/', index, name='index'),
    path('profil/<int:visiteur_id>/',profil_visiteur, name='profil_visiteur'),
]
