
import numpy as np
from datetime import datetime
import json
import random

from django.conf import settings
from shared.services.data_service import DataService
from shared.models import StepType

def create_survey_for_user(user_code):
    data_service = DataService()
    conversations = get_random_conversations(data_service)
    data_service.create_user_survey(conversations, user_code)


def get_random_conversations(service):
    human_conversations = service.get_human_conversations()
    machine_conversations = service.get_machine_conversations()
    num_of_conversations_per_survey = settings.NUM_OF_CONVERSATIONS_PER_SURVEY
    np.random.shuffle(human_conversations)
    np.random.shuffle(machine_conversations)

    conversations_h = human_conversations[:num_of_conversations_per_survey-1]
    conversation_m = machine_conversations[:1][0]

    rand_order_of_conversation_m = random.randint(0, num_of_conversations_per_survey-1)

    conversations = []
    
    conversations.extend(conversations_h)
    conversations.insert(rand_order_of_conversation_m, conversation_m)

    return conversations


def get_user_by_code(code):
    if not code:
        return None
    
    data_service = DataService()
    return data_service.get_user_by_code(code)


def get_next_survey_steps(data_service, code):
    survey_steps = data_service.get_user_survey_steps_by_user_code(code)
    next_step_ind = -1
    for ind, step in enumerate(survey_steps):
        step_not_done = step['end_time'] is None or datetime.fromtimestamp(float(step['end_time']) / 1000.0) > datetime.now()
        if step_not_done:
            next_step_ind = ind
            break
    
    if next_step_ind == -1:
        return None
    
    add_start_and_end_step(survey_steps, next_step_ind)

    return survey_steps[next_step_ind:]


def add_start_and_end_step(survey_steps, next_step_ind):
    survey_not_started = next_step_ind == 0 and survey_steps[0]['start_time'] is None
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
        start_time, user_code, conversation_end_time = payload['start_time'], payload['user_code'], payload['conversation_end_time']
        user = get_user_by_code(user_code)
        if not user:
            return False, []        
        return True, [start_time, user_code, conversation_end_time]
    except:
        return False, []


def start_survey_by_user(data):
    start_time, user_code, conversation_end_time = data
    data_service = DataService()
    data_service.start_survey(start_time, user_code, conversation_end_time)

def get_rate_conversation_data(request):
    try:
        payload = json.loads(request.body)
        conversation_code, end_time, rating, user_code = payload['conversation_code'], payload['end_time'], payload['rating'], payload['user_code']
        user = get_user_by_code(user_code)
        if not user:
            return False, []        
        return True, [conversation_code, end_time, rating, user_code]
    except:
        return False, []


def rate_conversation_by_user(data):
    data_service = DataService()
    data_service.rate_conversation(data)


def get_give_reason_data(request):
    try:
        payload = json.loads(request.body)
        conversation_code, user_code, reason, conversation_start_time, conversation_end_time, started_conversation_code = \
        payload['conversation_code'], payload['user_code'], payload['reason'], payload['conversation_start_time'], payload['conversation_end_time'], payload['started_conversation_code']
        user = get_user_by_code(user_code)
        if not user:
            return False, []        
        return True, [conversation_code, user_code, reason, conversation_start_time, conversation_end_time, started_conversation_code]
    except:
        return False, []

def give_reason_by_user(data):
    data_service = DataService()
    data_service.give_reason(data)


def get_end_survey_data(request):
    try:
        payload = json.loads(request.body)
        user_code = payload['user_code']
        user = get_user_by_code(user_code)
        if not user:
            return False, None       
        return True, user_code
    except:
        return False, None

def end_user_survey(user_code):
    data_service = DataService()
    data_service.end_user_survey(user_code)


def get_reset_survey_data(request):
    try:
        payload = json.loads(request.body)
        code = payload['code']
        user = get_user_by_code(code)
        if not user:
            return False, None       
        return True, code
    except:
        return False, None

def reset_user_survey(user_code):
    data_service = DataService()
    data_service.reset_user_survey(user_code)