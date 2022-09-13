from django.db import models
from users.models import Profile
import uuid
from datetime import datetime


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created_by = models.ForeignKey(Profile, related_name='created_by', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=True, max_length=100)
    group_users = models.ManyToManyField(Profile, through='GroupUser')
    last_update = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class GroupUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    balance = models.FloatField(default=0)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.full_name


class TransferToMake(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    sender = models.ForeignKey(GroupUser, related_name='borrower', on_delete=models.CASCADE, blank=True)
    amount = models.FloatField(blank=True)
    receiver = models.ForeignKey(GroupUser, on_delete=models.CASCADE, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.sender.profile} owes {self.amount} to {self.receiver.profile}'


class Expense(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    title = models.CharField(null=True, max_length=100)
    price = models.FloatField(null=True)
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    paid_date = models.DateTimeField(default=datetime.now(), null=True)
    paid_by = models.ForeignKey(GroupUser, related_name='paid_by', on_delete=models.CASCADE, null=True)
    split_with = models.ManyToManyField(GroupUser, related_name='expense_split')
    created_by = models.ForeignKey(GroupUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


class ExpenseComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(GroupUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(max_length=250, null=True, blank=True)

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True)


class CashMovement(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    group_user = models.ForeignKey(GroupUser, on_delete=models.CASCADE, null=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True)
    balance_impact = models.FloatField(null=True)