from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, data):
        print(data)
        user = User(**data)

        user.set_password(data['password'])
        print(data['password'])
        user.save()

        return user


# class RegisterUserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }
#
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError("Пароли не совпадают.")
#         return data
#
#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

# ----------------------------------------------------------------------------------------------------------------------

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
