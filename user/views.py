
from django.http import JsonResponse, HttpResponseNotAllowed, Http404

from survey.services.survey_service import create_survey_for_user
from .permissions import is_allowed_to_register
from .services.user_service import get_registration_code


@is_allowed_to_register
def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    
    success, code = get_registration_code(request)
    if not success:
        return Http404()

    create_survey_for_user(code)
    return JsonResponse({'message': 'OK', 'content': {'registration_code': code}})
