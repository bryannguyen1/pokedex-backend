from .views import RegisterAPI, LoginAPI
from knox import views as knox_views
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/pokemon/<str:pokemonName>/', views.pokemon, name="pokemon"),
    path('api/allfavoritepokemon/', views.allfavoritepokemon, name="allfavoritepokemon"),
    path('api/favoritepokemon/', views.favoritepokemon, name="favoritepokemon"),
    path('api/pokemon/<str:pokemonName>/favorite/', views.favorite, name="favorite"),
]