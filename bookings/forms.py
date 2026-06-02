from django import forms
from .models import Booking
from services.models import Service

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'project_title', 'project_description', 'budget', 'deadline', 'requirement_file']
        widgets = {
            'service': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'e.g., Corporate Commercial Video'
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 h-32 resize-none',
                'placeholder': 'Describe your requirements, goals, references...'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'e.g., 1500.00'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'type': 'date'
            }),
            'requirement_file': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 cursor-pointer'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(active=True)
        # Custom display for services:
        self.fields['service'].empty_label = "-- Choose a Service Type --"
