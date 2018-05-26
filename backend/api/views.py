from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from core.models import Event

from api import serializers


class ObtainUserAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_profile_serializer = serializers.UserProfileSerializer(
            instance=user)

        return Response({
            'token': token.key,
            'profile': user_profile_serializer.data
        })


obtain_auth_token = ObtainUserAuthToken.as_view()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EventCreateSerializer
        return self.serializer_class


class EventStatusViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.ChoiceSerializer

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        items = [{'id': key, 'name': value} for key, value in
                 Event.STATUS]

        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
