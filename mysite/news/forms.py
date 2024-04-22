from django import forms

class TagForm(forms.Form):
    tag = forms.CharField(label="Тэг",widget=forms.Textarea(attrs={"rows": 1}))