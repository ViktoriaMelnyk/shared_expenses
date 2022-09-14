from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    paid_date = forms.DateTimeField(widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M'))

    class Meta:
        model = Expense
        fields = [
            'title',
            'price',
            'paid_date',
            'paid_by',
            'split_with',
            'comment'
        ]
        widgets = {
            'split_with': forms.CheckboxSelectMultiple(),
        }