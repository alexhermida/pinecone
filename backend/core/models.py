from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class Event(TimeStampedModel):
    STATUS = Choices(('draft', _('draft')), ('published', _('published')))

    description = models.TextField(_('description'))
    group = models.TextField(_('group'))
    link = models.TextField(_('link'))
    location = models.TextField(_('location'))
    status = StatusField(_('status'))
