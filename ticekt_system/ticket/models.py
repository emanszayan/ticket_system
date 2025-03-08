from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from customer.models import Customer

User = get_user_model()


class Ticket(models.Model):
    PRIORITY_CHOICES = (
        (1, _('1. Critical')),
        (2, _('2. High')),
        (3, _('3. Normal')),
        (4, _('4. Low')),
        (5, _('5. Very Low')),
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=200,
    )

    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True,
        help_text=_('Date this ticket was first created'),
    )

    customer = models.ForeignKey(
        to=Customer, on_delete=models.SET_NULL,
        blank=False, null=True,
        verbose_name="Customer"
    )
    is_sold = models.BooleanField(
        verbose_name=_("Is Sold"),
        default=False)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assigned_to',
        null=True,
        verbose_name=_('Assigned to'),
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
        help_text=_('The content of the customers query.'),
    )

    priority = models.IntegerField(
        verbose_name=_('Priority'),
        choices=PRIORITY_CHOICES,
        default=3,
        blank=3,
        help_text=_('1 = Highest Priority, 5 = Low Priority'),
    )
    price = models.DecimalField(
        verbose_name=_('Price'),
        max_digits=10,
        decimal_places=2)
    event_date = models.DateTimeField(
        verbose_name=_('Event Date')
    )

    class Meta:
        ordering = ('id',)
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return "{} - {}".format(self.id, self.title)
