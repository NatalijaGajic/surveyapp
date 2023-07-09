
import numpy as np
from datetime import datetime

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
            conversation_code = step['conversation']
            step['conversation'] = data_service.get_conversation_by_code(conversation_code)

    return survey_steps




