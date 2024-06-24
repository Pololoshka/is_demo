from django.shortcuts import render

from duplicatefinder.forms import ChoiceModelForm
from duplicatefinder.handlers import find_duplicates, MODELS_DATA
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def find_duplicates_for_models(request):
    but = request.bitrix_user_token
    duplicates, model_name = None, None
    if request.GET:
        model_name = MODELS_DATA[request.GET['model']]['model_name']
        duplicates = find_duplicates(but=but, selected_model=request.GET['model'])
    form = ChoiceModelForm()
    return render(request, 'duplicates.html', context={'form': form, 'duplicates': duplicates, 'model': model_name}, )
