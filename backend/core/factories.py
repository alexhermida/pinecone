import factory

from core import models


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    description = factory.Faker('text')
    group = factory.Faker('text')
    link = factory.Faker('text')
    location = factory.Faker('text')
    status = factory.Faker('text')
