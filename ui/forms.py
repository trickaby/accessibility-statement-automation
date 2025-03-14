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
    temperature = forms.CharField(
        label="Temperature",
        initial=0.2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
    )
    top_k = forms.CharField(
        label="Top-K",
        initial=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
    )
    top_p = forms.CharField(
        label="Top-P (Nucleus sampling)",
        initial=0.3,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
    )
    max_tokens = forms.CharField(
        label="Max tokens",
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
    )
    repetition_penalty = forms.CharField(
        label="Repetition Penalty",
        initial=1.2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ai-config'}),
    )

    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')
        if temperature:
            try:
                temperature = float(temperature)
                if not (0.0 <= temperature <= 2.0):
                    raise ValidationError("Temperature must be between 0.0 and 2.0.")
                return temperature
            except (ValueError, TypeError):
                raise ValidationError("Temperature must be a valid number.")

    def clean_top_k(self):
        top_k = self.cleaned_data.get('top_k')
        if top_k:
            try:
                top_k = float(top_k)
                if not (0.0 <= top_k <= 1000.0):
                    raise ValidationError("Top-K must be between 0.0 and 1000.0.")
                return top_k
            except (ValueError, TypeError):
                raise ValidationError("Top-K must be a valid number.")

    def clean_top_p(self):
        top_p = self.cleaned_data.get('top_p')
        if top_p:
            try:
                top_p = float(top_p)
                if not (0.0 <= top_p <= 1.0):
                    raise ValidationError("Top-P must be between 0.0 and 1.0.")
                return top_p
            except (ValueError, TypeError):
                raise ValidationError("Top-P must be a valid number.")

    def clean_max_tokens(self):
        max_tokens = self.cleaned_data.get('max_tokens')
        if max_tokens :
            try:
                max_tokens = float(max_tokens)
                if not (-2.0 <= max_tokens <= 131072.0):
                    raise ValidationError("Max tokens must be between -2.0 and 131072.0.")
                return max_tokens
            except (ValueError, TypeError):
                raise ValidationError("Max tokens must be a valid number.")

    def clean_repetition_penalty(self):
        repetition_penalty = self.cleaned_data.get('repetition_penalty')
        if repetition_penalty:
            try:
                repetition_penalty = float(repetition_penalty)
                if not (-2.0 <= repetition_penalty <= 2.0):
                    raise ValidationError("Repetition Penalty must be between -2.0 and 2.0.")
                return repetition_penalty
            except (ValueError, TypeError):
                raise ValidationError("Repetition Penalty must be a valid number.")

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