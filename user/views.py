
from django.http import JsonResponse, HttpResponseNotAllowed, Http404

from survey.services.survey_service import create_survey_for_user, get_user_by_code
from .permissions import is_allowed_to_register
from .services.user_service import get_registration_data, get_registration_code, add_user
from shared.services.logging_service import prepare_request_log


import logging

logger = logging.getLogger("django")


@is_allowed_to_register
def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    
    try:
        success, registration_data = get_registration_data(request)
        if not success:
            logger.error(prepare_request_log(request))
            logger.exception("An error occurred")
            return JsonResponse({'message': 'ERROR', 'content': {}})
    
        code = get_registration_code(registration_data)
        user = get_user_by_code(code)
        if user:
            return JsonResponse({'message': 'OK', 'content': {'registration_code': code}})
        
        registration_data.extend([code, False])
        add_user(registration_data)

        create_survey_for_user(code)

        return JsonResponse({'message': 'OK', 'content': {'registration_code': code}})
    except Exception as ex:
        logger.error(prepare_request_log(request))
        logger.exception("An error occurred")
        return JsonResponse({'message': 'ERROR', 'content': {'exception_message': str(ex)}})


