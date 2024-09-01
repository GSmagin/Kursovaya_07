from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status
from users.serializers import UserProfileTelegramSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response

User = get_user_model()


# Авторизация пользователя (получение токена)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)  # Создание access_token напрямую
            return Response({
                'refresh': str(refresh),
                'access': str(access),
            })
        return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)


# Регистрация пользователя
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if email and password:
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
            return Response({"message": "Пользователь успешно создан"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Требуется адрес электронной почты и пароль"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileTelegramView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileTelegramSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

