
import numpy as np
from datetime import datetime
import json

from django.conf import settings
from shared.services.data_service import DataService
from shared.models import StepType

def create_survey_for_user(user_code):
    data_service = DataService()
    conversations = get_random_conversations(data_service)
    data_service.create_user_survey(conversations, user_code)


def get_random_conversations(service):
    conversations = service.get_conversations()
    num_of_conversations_per_survey = settings.NUM_OF_CONVERSATIONS_PER_SURVEY
    np.random.shuffle(conversations)
    return conversations[:num_of_conversations_per_survey]


def get_user_by_code(code):
    if not code:
        return None
    
    data_service = DataService()
    return data_service.get_user_by_code(code)


def get_next_survey_steps(data_service, code):
    survey_steps = data_service.get_user_survey_steps_by_user_code(code)
    next_step_ind = -1
    for ind, step in enumerate(survey_steps):
        step_not_done = step['end_time'] is None or step['end_time'] > datetime.now()
        if step_not_done:
            next_step_ind = ind
            break
    
    if next_step_ind == -1:
        return None
    
    add_start_and_end_step(survey_steps, next_step_ind)

    return survey_steps[next_step_ind:]


def add_start_and_end_step(survey_steps, next_step_ind):
    survey_not_started = next_step_ind == 0
    if survey_not_started:
        survey_steps.insert(0, {'type': StepType.START.value})
    survey_steps.append({'type': StepType.END.value})


def get_survey_steps_to_show(user_code):
    
    data_service = DataService()

    survey_steps = get_next_survey_steps(data_service, user_code)
    for step in survey_steps:
        if step['type'] == StepType.CONVERSATION.value:
            step['duration_in_seconds'] = settings.SECONDS_PER_CONVERSATION
            conversation_code = step['conversation_code']
            step['conversation'] = data_service.get_conversation_by_code(conversation_code)

    return survey_steps



def get_start_survey_data(request):
    try:
        payload = json.loads(request.body)
        start_time, user_code = payload['start_time'], payload['user_code']
        user = get_user_by_code(user_code)
        if not user:
            False, []        
        return True, [start_time, user_code]
    except:
        False, []


def start_survey_by_user(data):
    start_time, user_code = data
    data_service = DataService()
    data_service.start_survey(start_time, user_code) # TODO add start_survey (find user_survey, add start_time to first conversation)

def get_rate_conversation_data(request):
    try:
        payload = json.loads(request.body)
        conversation_code, end_time, rating, user_code = payload['conversation_code'], payload['end_time'], payload['rating'], payload['user_code']
        user = get_user_by_code(user_code)
        if not user:
            False, {}        
        return True, {'conversation_code': conversation_code, 'end_time': end_time, 'rating': rating, 'user_code': user_code}
    except:
        False, {}


def rate_conversation(data):
    data_service = DataService()
    data_service.rate_conversation(data) # TODO add rate_conversation (find user_survey, add end_time, rating to conversation)


def get_give_reason_data(request):
    try:
        payload = json.loads(request.body)
        conversation_code, user_code, reason, conversation_start_time = payload['conversation_code'], payload['user_code'], payload['reason'], payload['conversation_start_time']
        user = get_user_by_code(user_code)
        if not user:
            False, {}        
        return True, {'conversation_code': conversation_code, 'reason': reason, 'user_code': user_code, 'conversation_start_time': conversation_start_time}
    except:
        False, {}

def give_reason(data):
    data_service = DataService()
    data_service.give_reason(data) # TODO add give_reason (find user_survey, add start_time to next conversation, reason to conversation)


def get_end_survey_data(request):
    try:
        payload = json.loads(request.body)
        end_time, user_code =payload['end_time'], payload['user_code']
        user = get_user_by_code(user_code)
        if not user:
            False, {}        
        return True, { 'end_time': end_time, 'user_code': user_code}
    except:
        False, {}

def end_survey(data):
    data_service = DataService()
    data_service.end_survey(data) # TODO add end_survey (find user, update survey_done)