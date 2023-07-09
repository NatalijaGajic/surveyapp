from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, Http404, JsonResponse

from .services.survey_service import get_user_by_code, get_survey_steps_to_show, get_start_survey_data, start_survey_by_user, get_rate_conversation_data, get_give_reason_data, give_reason, get_end_survey_data, end_survey


def index(request):
    code = request.GET.get('code', None) 
    user = get_user_by_code(code)

    if not user or (user and user['survey_done']):
        return HttpResponseForbidden()
    
    survey_steps = get_survey_steps_to_show(code)
    return render(request, 'index.html', context = {'steps': survey_steps})


def start_survey(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    
    success, data = get_start_survey_data(request)
    if not success:
        return Http404()
    
    start_survey_by_user(data)
    
    return JsonResponse({'message': 'OK', 'content': {}})

def rate_conversation(request):
    success, data = get_rate_conversation_data(request)
    if not success:
        return Http404()
    
    rate_conversation(data)

    return JsonResponse({'message': 'OK', 'content': {}})


def give_reason(request):
    success, data = get_give_reason_data(request)
    if not success:
        return Http404()
    
    give_reason(data)
    return JsonResponse({'message': 'OK', 'content': {}})


def end_survey(request):
    success, data = get_end_survey_data(request)
    if not success:
        return Http404()
    
    end_survey(data)
    return JsonResponse({'message': 'OK', 'content': {}})