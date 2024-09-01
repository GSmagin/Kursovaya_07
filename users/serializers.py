from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['telegram_chat_id', 'telegram_token']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Не обязательное поле

    class Meta:
        model = User
        # fields = ['email', 'first_name', 'last_name', 'password']  # Убедитесь, что все поля актуальны
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=password
        )
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
