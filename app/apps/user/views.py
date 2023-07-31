from rest_framework import permissions, status
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from apps.user.serializers import UserRegisterSerializer , UserSerializer , ChangePasswordSerializer
from apps.user.validations import custom_validation


class UserRegister(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password changed successfully."})

        return Response(serializer.errors, status=400)
