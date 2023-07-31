from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()


def custom_validation(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        raise ValidationError('Please provide username, email, and password.')

    if UserModel.objects.filter(username=username).exists():
        raise ValidationError('Username already exists.')

    if UserModel.objects.filter(email=email).exists():
        raise ValidationError('Email address already registered.')

    return data