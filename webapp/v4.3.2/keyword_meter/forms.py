from django import forms
from keyword_meter.models import GHResultKeywordMeter


class GHResultKeywordMeterForm(forms.ModelForm):
    class Meta:
        model = GHResultKeywordMeter
        exclude = [
            ''
        ]
