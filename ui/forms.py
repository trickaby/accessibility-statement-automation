from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator

from accessibility_web import settings


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Upload a CSV File",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )
    headless_mode = forms.BooleanField(label="Run Headless", required=False)
    enable_ai = forms.BooleanField(
        label="Enable AI analysis of non-accessible content",
        required=False,
        widget=forms.CheckboxInput(attrs={'onchange': "toggleAIConfig()"})
    )
    ai_model = forms.CharField(
        label="AI Model",
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'})
    )
    system_prompt = forms.CharField(
        label="System prompt",
        initial=settings.DEFAULT_SYSTEM_PROMPT,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'ai-config',
                'rows': '15',
                'cols': '100'
            },
        )
    )
    temperature = forms.FloatField(
        label="Temperature",
        initial=0.2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)]
    )
    top_k = forms.FloatField(
        label="Top-K",
        initial=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
        validators=[MinValueValidator(0.0), MaxValueValidator(1000.0)]
    )
    top_p = forms.FloatField(
        label="Top-P (Nucleus sampling)",
        initial=0.3,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    max_tokens = forms.FloatField(
        label="Max tokens",
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
        validators=[MinValueValidator(-2.0), MaxValueValidator(131072.0)]
    )
    repetition_penalty = forms.FloatField(
        label="Repetition Penalty",
        initial=1.2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
        validators=[MinValueValidator(-2.0), MaxValueValidator(2.0)]
    )

    def clean(self):
        cleaned_data = super().clean()
        enable_ai = cleaned_data.get('enable_ai')
        ai_model = cleaned_data.get('ai_model')

        if enable_ai and not ai_model:
            raise ValidationError({
                'ai_model': "AI Model is required."
            })

        ai_config_fields = ['temperature', 'top_k', 'top_p', 'max_tokens',
                            'repetition_penalty']
        options = {field: cleaned_data.pop(field) for field in ai_config_fields if field in cleaned_data}

        cleaned_data['options'] = options

        return cleaned_data