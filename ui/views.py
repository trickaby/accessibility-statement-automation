from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import HttpResponse

from .logic import run_logic, output_db_to_csv
from accessibility_scraper.src.modules.ollama_config import OllamaConfig
from accessibility_scraper.src.modules.scraper_config import ScraperConfig
from .forms import UploadFileForm
import os



def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            headless_mode = form.cleaned_data['headless_mode']

            # enable_ai = form.cleaned_data['enable_ai']

            ollama_config = None
            # if enable_ai:
            #     ai_model = form.cleaned_data['ai_model']
            #     system_prompt = form.cleaned_data['system_prompt']
            #     options = form.cleaned_data['options']
            #     ollama_config = OllamaConfig(ai_model, system_prompt, options)
            config = ScraperConfig(headless_mode, ollama_config)
            try:
                run_logic(config)
                return render(request, 'scraper/result.html', {
                    'output_file': output_db_to_csv()
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