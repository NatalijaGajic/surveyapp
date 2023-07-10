from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse

from .services.survey_service import get_user_by_code, get_survey_steps_to_show, get_start_survey_data, start_survey_by_user, \
    get_rate_conversation_data, rate_conversation_by_user, get_give_reason_data, give_reason_by_user, get_end_survey_data, \
    end_user_survey, get_reset_survey_data, reset_user_survey

from user.permissions import is_allowed_to_reset_survey

def index(request):
    code = request.GET.get('code', None) 
    user = get_user_by_code(code)

    if not user:
        return HttpResponseForbidden()
    
    if user['survey_done']:
        return render(request, 'index.html', context = {'steps': [{'type': 'end'}], 'code': code})
    
    survey_steps = get_survey_steps_to_show(code)
    return render(request, 'index.html', context = {'steps': survey_steps, 'code': code})


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


@is_allowed_to_reset_survey
def reset_survey(request):

    success, code = get_reset_survey_data(request)
    if not success:
        return HttpResponseBadRequest()
    
    reset_user_survey(code)

    return JsonResponse({'message': 'OK', 'content': {}})