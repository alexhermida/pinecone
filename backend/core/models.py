from django.contrib.auth.models import User

from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class Event(TimeStampedModel):
    STATUS = Choices(('draft', _('draft')), ('published', _('published')))

    title = models.TextField(_('title'), null=True)
    description = models.TextField(_('description'))
    group = models.TextField(_('group'))
    link = models.TextField(_('link'))
    location = models.TextField(_('location'))
    status = StatusField(_('status'))

    start = models.DateTimeField(_('start'), null=True, blank=True)
    end = models.DateTimeField(_('end'), null=True, blank=True)

    user = models.ForeignKey(User, null=True, verbose_name=_('user'),
                             on_delete=models.PROTECT)

    google_calendar_published = models.BooleanField(_('google_cal_published'),
                                                    default=False)
    google_event_id = models.TextField(_('google event id'), null=True)
