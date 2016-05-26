
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

STOP_TYPES = (
    (1, _("stop_position")),
    (2, _("platform"))
    )