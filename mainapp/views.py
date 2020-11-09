from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    RetrieveUpdateAPIView, CreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from mainapp.license import IsOwnerProfileOrReadOnly
from mainapp.models import Profile, Service, Masters
from mainapp.serializers import SerializerUserRegistration, UserSerializerView, ProfileUserSerializerView, \
    SerializerServiceRegistration, SerializerCreateServiceCreate, SerializerMasters, \
    SerializerServiceCreate, SerializerMasterPreView
from django.contrib.auth.models import User
from djoser.conf import User


class MainIndexView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializerView(queryset, many=True)
        return Response(serializer.data)


class UserProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUserSerializerView


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUserSerializerView
    permission_classes = [IsOwnerProfileOrReadOnly, AllowAny]


class ProfileUserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUserSerializerView

    def get_object(self):
        return self.request.user


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
            data['password'] = new_user.password
            data['token'] = Profile.get_tokens_for_user(new_user)
        else:
            serializer.errors
        return Response(data)


class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request):
        queryset = Service.objects.filter(client_to_job=self.get_object())
        serializer_class = SerializerServiceRegistration(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        queryset = Service.objects.filter(client_to_job=self.get_object())
        serializer = SerializerServiceRegistration(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerCreateServiceCreate

    def get_object(self):
        return self.request.user


class PreviewMastersView(APIView):

    def get(self, request):
        queryset = Service.objects.all()
        serializer_class = SerializerMasterPreView(queryset, many=True)
        return Response(serializer_class.data)



