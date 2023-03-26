from django import forms
from .models import TODO

# class TodoForm(forms.Form):
#     title = forms.CharField(max_length=20)
#     content = forms.CharField(widget=forms.Textarea)

class TodoForm(forms.ModelForm):

    class Meta:
        model = TODO
        fields = '__all__'