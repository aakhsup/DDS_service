from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        t = cleaned_data.get('type')

        if category and category.type != t:
            raise forms.ValidationError("Категория не соответствует выбранному типу.")
        if subcategory and subcategory.category != category:
            raise forms.ValidationError("Подкатегория не соответствует выбранной категории.")
        return cleaned_data
