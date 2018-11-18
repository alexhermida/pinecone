from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class Group(models.Model):
    name = models.TextField(_('name'))
    logo = models.TextField(_('logo'))
    links = JSONField(_('links'))


class Event(TimeStampedModel):
    STATUS = Choices(('draft', _('draft')), ('published', _('published')))

    title = models.TextField(_('title'), null=True)
    description = models.TextField(_('description'))
    link = models.TextField(_('link'))
    location = models.TextField(_('location'))
    status = StatusField(_('status'))

    start = models.DateTimeField(_('start'), null=True, blank=True)
    end = models.DateTimeField(_('end'), null=True, blank=True)
    duration = models.IntegerField(_('duration'), null=True, blank=True)

    user = models.ForeignKey(User, null=True, verbose_name=_('user'),
                             on_delete=models.PROTECT)

    google_calendar_published = models.BooleanField(_('google_cal_published'),
                                                    default=False)
    google_event_id = models.TextField(_('google event id'), null=True)
    google_event_htmllink = models.TextField(_('google event link'), null=True)

    import_id = models.TextField(_('import event id'), null=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
