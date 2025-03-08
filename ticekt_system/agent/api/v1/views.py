from rest_framework.generics import (GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     DestroyAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.utils.translation import gettext_lazy as _
from .serializers import PasswordChangeSerializer,UserSerializer
from django.contrib.auth import get_user_model
from .permissions import IsSuperUser
User = get_user_model()

class AuthTokenGenerator(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        login api to generate token for user
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate or get the token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


class LogOut(DestroyAPIView):
    """
    Logout user by deleting his own token
    it deletes the current authenticated user's token
    """
    permission_classes = [IsAuthenticated]
    queryset = Token.objects.all()

    def get_object(self):
        return Token.objects.get(user=self.request.user)


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2',
    ),
)


class PasswordChangeView(GenericAPIView):
    """
    change password for any user
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('New password has been saved.')})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_user_password(request, pk):
    """
    change current login user password
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'detail': _('User not found.')}, status=404)

    new_password1 = request.data.get('new_password1')
    new_password2 = request.data.get('new_password2')

    if new_password1 and new_password2:
        if new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()

            return Response({'detail': _('New password has been saved.')})
        else:
            return Response({'detail': _('Passwords do not match.')})
    else:
        return Response({'detail': _('Both new_password1 and new_password2 are required.')}, status=400)

class UserListCreateAPIView(ListCreateAPIView):
    """
    list and create user permission for admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =[IsSuperUser]

# Retrieve, Update, Delete a Single User
class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    get,delete and update user permission for admin

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =[IsSuperUser]