"""
Views for user API
"""
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user API view
    """

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Create token for user
    """

    serializer_class = AuthTokenSerializer
    # to be shown in the documentation nicely we can add renderer class as below:
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Manage authenticated user
    """

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return authenticated user
        :return: user
        """
        return self.request.user
