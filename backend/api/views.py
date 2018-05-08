from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response

from api import serializers

from core.models import Event


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer


class EventStatusViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.ChoiceSerializer

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        items = [{'id': key, 'name': value} for key, value in
                 Event.STATUS]

        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

