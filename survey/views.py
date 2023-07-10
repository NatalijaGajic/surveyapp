from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse

from .services.survey_service import get_user_by_code, get_survey_steps_to_show, get_start_survey_data, start_survey_by_user, \
    get_rate_conversation_data, rate_conversation_by_user, get_give_reason_data, give_reason_by_user, get_end_survey_data, end_user_survey


def index(request):
    code = request.GET.get('code', None) 
    user = get_user_by_code(code)

    if not user:
        return HttpResponseForbidden()
    
    if user['survey_done']:
        return render(request, 'index.html', context = {'steps': [{'type': 'end'}]})
    
    survey_steps = get_survey_steps_to_show(code)
    return render(request, 'index.html', context = {'steps': survey_steps})


def start_survey(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    
    success, data = get_start_survey_data(request)
    if not success:
        return HttpResponseBadRequest()
    
    start_survey_by_user(data)
    
    return JsonResponse({'message': 'OK', 'content': {}})

def rate_conversation(request):
    success, data = get_rate_conversation_data(request)
    if not success:
        return HttpResponseBadRequest()
    print('view')
    rate_conversation_by_user(data)

    return JsonResponse({'message': 'OK', 'content': {}})


def give_reason(request):
    success, data = get_give_reason_data(request)
    if not success:
        return HttpResponseBadRequest()
    
    give_reason_by_user(data)
    return JsonResponse({'message': 'OK', 'content': {}})


def end_survey(request):
    success, data = get_end_survey_data(request)
    if not success:
        return HttpResponseBadRequest()
    
    end_user_survey(data)
    return JsonResponse({'message': 'OK', 'content': {}})