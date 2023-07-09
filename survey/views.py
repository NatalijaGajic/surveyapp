from django.shortcuts import render
from django.http import HttpResponseForbidden

from .services.survey_service import get_user_by_code, get_survey_steps_to_show


def index(request):
    code = request.GET.get('code', None) 
    user = get_user_by_code(code)

    if not user or (user and user['survey_done']):
        return HttpResponseForbidden()
    
    survey_steps = get_survey_steps_to_show(code)
    return render(request, 'index.html', context = {'steps': survey_steps})


def answer(request):
    pass