from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdministrator
from .serializers import EmailSerializer, UserCodeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdministrator,)
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user,
            request.data,
            partial=True
        )
        user = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_code(request):
    """Validate username, email and send confirmation code to email."""
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    if username == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(Q(email=email) | Q(username=username)).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user, created = User.objects.get_or_create(
        email=email,
        username=username
    )
    confirmation_code = PasswordResetTokenGenerator().make_token(user)
    send_mail('Confirmation code for receiving a token',
              confirmation_code,
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Validate username, confirmation code and return token."""
    serializer = UserCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if PasswordResetTokenGenerator().check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response(
        'You entered an incorrect email or incorrect verification code',
        status=status.HTTP_400_BAD_REQUEST)
