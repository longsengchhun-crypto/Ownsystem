from django import forms
from .models import Project, ProjectFile

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['assigned_team', 'progress_percentage', 'notes', 'completion_date']
        widgets = {
            'assigned_team': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 h-24 resize-none',
                'placeholder': 'e.g., John Doe (Lead Shooter), Sam Smith (Editor)'
            }),
            'progress_percentage': forms.NumberInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'min': '0',
                'max': '100'
              }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 h-32 resize-none',
                'placeholder': 'Add update notes, production statuses, or directions for the client...'
            }),
            'completion_date': forms.DateInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'type': 'date'
            })
        }


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 cursor-pointer'
            })
        }
