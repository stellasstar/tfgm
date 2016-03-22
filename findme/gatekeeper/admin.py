from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from gatekeeper.models import User
from gatekeeper.forms import RegistrationForm, CustomUserChangeForm


admin.site.register(User)
