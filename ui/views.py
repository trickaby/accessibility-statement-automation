from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import HttpResponse

from accessibility_scraper.src.main import run_logic
from accessibility_scraper.src.modules.ollama_config import OllamaConfig
from accessibility_scraper.src.modules.scraper_config import ScraperConfig
from .forms import UploadFileForm
import os



def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = default_storage.save(f"uploads/{file.name}", file)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            headless_mode = form.cleaned_data['headless_mode']

            output_file_path = os.path.join(settings.MEDIA_ROOT, f"Results_{file.name}")

            enable_ai = form.cleaned_data['enable_ai']

            ollama_config = None
            if enable_ai:
                ai_model = form.cleaned_data['ai_model']
                system_prompt = form.cleaned_data['system_prompt']
                options = form.cleaned_data['options']
                ollama_config = OllamaConfig(ai_model, system_prompt, options)
            config = ScraperConfig(file_path, output_file_path, headless_mode, ollama_config)
            try:
                result = run_logic(config)
                return render(request, 'scraper/result.html', {
                    'result': result,
                    'output_file': output_file_path
                })
            except Exception as e:
                return render(request, 'scraper/error.html', {
                    'error': str(e)
                })
    else:
        form = UploadFileForm()
    return render(request, 'scraper/home.html', {'form': form})

def download_result(request, file_path):
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response