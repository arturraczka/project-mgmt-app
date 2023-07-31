from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email = clean_data['email'], password = clean_data['password'],
                                                 username = clean_data['username'])
        user_obj.save()
        return user_obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        attrs = super().validate(attrs)
        new_password = attrs.get('new_password')
        self.validate_password(new_password)
        return attrs

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        if not any(char in "!@#$%^&*()-_=+~`[]{}|;:,.<>/?'\"" for char in password):
            raise serializers.ValidationError("Password must contain a special character.")

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain a number.")

        return password