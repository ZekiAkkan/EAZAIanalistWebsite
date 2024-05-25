# forms.py
from django import forms
from .models import SQLFile

class UploadSQLForm(forms.ModelForm):
    class Meta:
        model = SQLFile
        fields = ['file']
