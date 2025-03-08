from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Customer(models.Model):
    name = models.CharField(_('name'), max_length=128)
    mobile = models.CharField(_('Mobile'), max_length=20, unique=True)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   verbose_name=_('Created By'), editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
