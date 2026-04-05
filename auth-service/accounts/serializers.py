from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AdminUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = AdminUser
        fields = ['username', 'password']

    def create(self, validated_data):
        user = AdminUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                'Username and password are required'
            )

        user = AdminUser.objects.filter(
            username=username
        ).first()

        if not user:
            raise serializers.ValidationError(
                'Invalid username or password'
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Invalid username or password'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This account is disabled'
            )

        data['user'] = user
        return data