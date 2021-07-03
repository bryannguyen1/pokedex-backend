from django.shortcuts import render
from django.http import HttpResponse
from .models import PokemonEntry
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, PokemonEntrySerializer

def pokemon(request, pokemonName):
    existing = PokemonEntry.objects.filter(name=pokemonName)
    if not existing:
        entry = PokemonEntry(name=pokemonName, favorite=False)
        entry.save()
    entry = PokemonEntry.objects.filter(name=pokemonName).first()
    return JsonResponse({"name": pokemonName, "favorite": entry.favorite})

@api_view(['GET'])
def allfavoritepokemon(request):
    entries = PokemonEntry.objects.filter(favorite=True)
    serializer = PokemonEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def favoritepokemon(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    auser = serializer.validated_data['user']

    entries = PokemonEntry.objects.filter(favorite=True, user=auser)
    pSerializer = PokemonEntrySerializer(entries, many=True)
    return Response(pSerializer.data)

@api_view(['POST'])
def favorite(request, pokemonName):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    auser = serializer.validated_data['user']

    existing = PokemonEntry.objects.filter(name=pokemonName, user=auser)
    if not existing:
        entry = PokemonEntry(name=pokemonName, favorite=True, user=auser)
        entry.save()
    else:
        entry = PokemonEntry.objects.get(name=pokemonName, user=auser)
        entry.favorite = not entry.favorite
        entry.save()
    entry = PokemonEntry.objects.filter(name=pokemonName, user=auser).first()
    return JsonResponse({"name": pokemonName, "favorite": entry.favorite})

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)