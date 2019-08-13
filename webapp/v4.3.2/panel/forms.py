from django import forms
from panel.models import Code, GHResult, GHResult_LastVersions, Tag


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        exclude = [
            ''
        ]


class GHResultForm(forms.ModelForm):
    class Meta:
        model = GHResult
        exclude = [
            ''
        ]


class GHResultLastVersionsForm(forms.ModelForm):
    class Meta:
        model = GHResult_LastVersions
        exclude = [
            ''
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['']