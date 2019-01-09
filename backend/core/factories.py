import datetime as dt

from django.utils import timezone

import factory
from core import models


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group

    name = factory.Faker('name')
    links = {}


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    description = factory.Faker('text')
    group = factory.SubFactory(GroupFactory)
    link = factory.Faker('text')
    location = factory.Faker('text')
    status = factory.Faker('random_element', elements=models.Event.STATUS)
    start = factory.LazyFunction(timezone.now)
    end = factory.LazyAttribute(lambda o: o.start + dt.timedelta(hours=1))
