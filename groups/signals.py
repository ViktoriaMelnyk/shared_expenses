from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Expense, CashMovement
from .utils import manage_transfers


@receiver(pre_delete, sender=Expense)
def delete_expense(sender, instance, **kwargs):
    expense = instance
    cash_movements = CashMovement.objects.filter(expense=expense)
    for balance_change in cash_movements:
        balance_change.group_user.balance = balance_change.group_user.balance - balance_change.balance_impact
        balance_change.group_user.save()
        balance_change.delete()

    manage_transfers(expense.group)