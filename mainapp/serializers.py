from django.contrib.auth.models import User
from djoser.conf import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from mainapp.models import Profile, Service, Masters


class UserSerializerView(serializers.ModelSerializer):
    info_car = serializers.CharField(source='profile.info_car')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'info_car']


class ProfileUserSerializerView(serializers.ModelSerializer):
    info_car = serializers.CharField(source='profile.info_car')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'info_car']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        obj = super(ProfileUserSerializerView, self).update(instance, validated_data)
        if profile_data:
            profile = instance.profile if hasattr(instance, 'profile') else Profile(user=instance)
            profile.info_car = profile_data.get('info_car')
            profile.save()
        return obj


class SerializerUserRegistration(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.save()
        return user


class SerializerMasters(serializers.ModelSerializer):

    class Meta:
        model = Masters
        fields = '__all__'


class SerializerServiceRegistration(serializers.ModelSerializer):
    name_master = SerializerMasters()
    client_to_job = UserSerializerView()
    work_on = serializers.models.CharField(choices=Service.worked_hours)

    class Meta:
        model = Service
        fields = '__all__'


class SerializerCreateServiceCreate(serializers.ModelSerializer):

    work_on = serializers.models.CharField(choices=Service.worked_hours)

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('client_to_job',)

    def create(self, validated_data):
        return Service.objects.create(
            name_master=validated_data.get('name_master'),
            client_to_job=self.context['request'].user,
            work_on=validated_data.get('work_on')
        )

    if work_on == '10:00':
        raise serializers.ValidationError({'Время': 'ВЫберите другое время не 1'})


class SerializerServiceCreate(SerializerCreateServiceCreate):
    name_master = SerializerMasters()
    client_to_job = UserSerializerView()
