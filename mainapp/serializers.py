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
    data_to_work = serializers.models.DateField()

    class Meta:
        model = Service
        fields = '__all__'


class SerializerCreateServiceCreate(serializers.ModelSerializer):
    work_on = serializers.models.CharField(choices=Service.worked_hours)
    data_to_work = serializers.models.DateField()

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('client_to_job',)

    def create(self, validated_data):
        return Service.objects.create(
            name_master=validated_data.get('name_master'),
            client_to_job=self.context['request'].user,
            work_on=validated_data.get('work_on'),
            data_to_work=validated_data.get('data_to_work')
        )

    def validate(self, data):
        all_value = Service.objects.filter(
            name_master_id=data['name_master'],
            work_on=data['work_on'],
            data_to_work=data['data_to_work']).exists()
        if all_value:
            raise serializers.ValidationError("Выберите другое время")
        return data


class SerializerServiceCreate(SerializerCreateServiceCreate):
    name_master = SerializerMasters()
    client_to_job = UserSerializerView()


class SerializerMasterPreView(serializers.ModelSerializer):
    name_master = serializers.CharField(source='name_master.name')
    work_on = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['name_master', 'work_on', 'data_to_work', 'client_to_job']

    def get_work_on(self, obj):
        return obj.get_work_on_display()

    def get_client_to_job(self, obj):
        return obj.client_to_job_on_display()