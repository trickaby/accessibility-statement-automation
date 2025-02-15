from django import forms
from django.core.exceptions import ValidationError


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload a CSV File")
    headless_mode = forms.BooleanField(label="Run Headless", required=False)
    enable_ai = forms.BooleanField(
        label="Enable AI analysis of non-accessible content",
        required=False,
        widget=forms.CheckboxInput(attrs={'onchange': "toggleAIConfig()"})
    )
    ai_model = forms.CharField(
        label="AI Model",
        required=False,
        widget=forms.TextInput(attrs={'disabled': True})
    )
    system_prompt = forms.CharField(
        label="System prompt",
        required=False,
        widget=forms.Textarea(attrs={'disabled': True})
    )

    def clean(self):
        cleaned_data = super().clean()
        enable_ai = cleaned_data.get('enable_ai')
        ai_model = cleaned_data.get('ai_model')

        if enable_ai and not ai_model:
            raise ValidationError({
                'ai_model': "AI Model is required."
            })

        return cleaned_data