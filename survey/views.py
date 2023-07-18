from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.conf import settings

from .services.survey_service import get_user_by_code, get_survey_steps_to_show, get_start_survey_data, start_survey_by_user, \
    get_rate_conversation_data, rate_conversation_by_user, get_give_reason_data, give_reason_by_user, get_end_survey_data, \
    end_user_survey, get_reset_survey_data, reset_user_survey

from user.permissions import is_allowed_to_reset_survey

from shared.services.logging_service import prepare_request_log

import logging

logger = logging.getLogger("django")


def index(request):
    try:
        code = request.GET.get('code', None) 
        user = get_user_by_code(code)
    
        if not user:
            return HttpResponseForbidden()
        
        if user['survey_done']:
            return render(request, 'index.html', context = {'steps': [{'type': 'end'}], 'code': code, 'seconds_per_conversation': settings.SECONDS_PER_CONVERSATION})
        
        survey_steps = get_survey_steps_to_show(code)
        return render(request, 'index.html', context = {'steps': survey_steps, 'code': code, 'seconds_per_conversation': settings.SECONDS_PER_CONVERSATION})
    except:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return render(request, 'index.html', context = {'steps': [{'type': 'error'}], 'code': None, 'seconds_per_conversation': None})


def start_survey(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    try:
        success, data = get_start_survey_data(request)
        if not success:
            logger.error(prepare_request_log(request))
            logger.exception("An error occurred")
            return JsonResponse({'message': 'ERROR', 'content': {}})
        
        start_survey_by_user(data)
        
        return JsonResponse({'message': 'OK', 'content': {}})
    except:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return JsonResponse({'message': 'ERROR', 'content': {}})
    
    
def rate_conversation(request):
    try:
        success, data = get_rate_conversation_data(request)
        if not success:
            logger.error(prepare_request_log(request))
            logger.exception("An error occurred")
            return JsonResponse({'message': 'ERROR', 'content': {}})

        rate_conversation_by_user(data)

        return JsonResponse({'message': 'OK', 'content': {}})
    except:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return JsonResponse({'message': 'ERROR', 'content': {}})


def give_reason(request):
    try:
        success, data = get_give_reason_data(request)
        if not success:
            logger.error(prepare_request_log(request))
            logger.exception("An error occurred")
            return JsonResponse({'message': 'ERROR', 'content': {}})
        
        give_reason_by_user(data)
        return JsonResponse({'message': 'OK', 'content': {}})
    except:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return JsonResponse({'message': 'ERROR', 'content': {}})


def end_survey(request):
    try:
        success, data = get_end_survey_data(request)
        if not success:
            logger.error(prepare_request_log(request))
            logger.exception("An error occurred")
            return JsonResponse({'message': 'ERROR', 'content': {}})
        
        end_user_survey(data)
        return JsonResponse({'message': 'OK', 'content': {}})
    except:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return JsonResponse({'message': 'ERROR', 'content': {}})


@is_allowed_to_reset_survey
def reset_survey(request):
    try:
        success, code = get_reset_survey_data(request)
        if not success:
            logger.error(prepare_request_log(request))
            logger.exception("An error occurred")
            return JsonResponse({'message': 'ERROR', 'content': {}})
        
        reset_user_survey(code)

        return JsonResponse({'message': 'OK', 'content': {}})
    except:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return JsonResponse({'message': 'ERROR', 'content': {}})