from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload a CSV File")
    headless_mode = forms.BooleanField(label="Run Headless", required=False)