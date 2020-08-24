from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from mainapp.serializers import SerializerUserRegistration, UserSerializerView
from django.contrib.auth.models import User
from djoser.conf import User


class MainIndexView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializerView(queryset, many=True)
        return Response(serializer.data)


class RegistrationUsersApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SerializerUserRegistration(data=request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            data['response'] = 'Ура ты создал нового персонажа, героя, человека, или не создал?'
            data['email'] = new_user.email
            data['username'] = new_user.username
        else:
            serializer.errors
        return Response(data)

