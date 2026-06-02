from django import forms
from .models import Quotation

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['amount', 'description', 'estimated_delivery_time']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': '0.00'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 h-32 resize-none',
                'placeholder': 'Provide cost breakdown, specifications, and scope inclusions...'
            }),
            'estimated_delivery_time': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'e.g., 5 business days'
            })
        }
