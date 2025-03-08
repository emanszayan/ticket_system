from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

#
class User(AbstractUser):
    mobile = models.CharField(verbose_name=_('mobile'), help_text=_('Mobile Number'), max_length=30, null=True,
                              blank=True)

    is_agent = models.BooleanField(
        default=False, verbose_name=_('Is Agent'), help_text=_('Specify if this user will act as agent'))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('id',)

    def __str__(self):
        return self.username
