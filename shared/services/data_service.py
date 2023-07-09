import pandas as pd
import numpy as np

from django.conf import settings
from shared.models import StepType


class DataService():

    all_users_columns = ['first_name', 'last_name', 'timestamp', 'code', 'survey_done']
    user_survey_columns = ['conversation', 'start_time', 'end_time', 'rating', 'reason']

    def get_conversations(self):
        conversations_df = pd.read_excel(settings.CONVERSATIONS_PATH)
        return conversations_df['code'].to_numpy()
    
    def create_user_survey(self, conversations, code):
        user_survey_df = pd.DataFrame(columns=self.user_survey_columns)
        user_survey_df['conversation'] = conversations
        file_path = settings.USERS_SURVEYS_DIR + r'\{}.xlsx'.format(code)
        user_survey_df.to_excel(file_path, engine='xlsxwriter', columns=self.user_survey_columns, index=False)

    def add_user(self, user_data):
        users_df = pd.read_excel(settings.USERS_PATH)
        index = len(users_df.index)
        users_df.loc[index] = user_data
        users_df.to_excel(settings.USERS_PATH, engine='xlsxwriter', columns=self.all_users_columns, index=False)

    
    def get_user_by_code(self, code):
        users_df = pd.read_excel(settings.USERS_PATH)
        user_with_code_exists = code in users_df['code'].tolist()
        if not user_with_code_exists:
            return None

        user =  users_df.loc[(users_df['code'] == code)].values[0]
        return {'first_name': user[0], 'last_name': user[1], 
                'timestamp': user[2], 'code': user[3], 'survey_done': user[4]}



    def get_conversation_by_code(self, code):
        conversations_df = pd.read_excel(settings.CONVERSATIONS_PATH)
        conversation_with_code_exists = code in conversations_df['code'].to_numpy()
        if not conversation_with_code_exists:
            return None
        
        file_path = settings.CONVERSATIONS_DIR + r'\{}.xlsx'.format(code)
        conversation_df = pd.read_excel(file_path)
        conversation = []
        for i in range(settings.NUM_OF_QUESTIONS_PER_CONVERSATION):
            qa_pair = conversation_df.iloc[i]
            question, answer = qa_pair['question'], qa_pair['answer']
            conversation.append({'question': question, 'answer': answer})
        return conversation
    

    def get_user_survey_steps_by_user_code(self, code):
        survey_df = self.get_user_survey_by_user_code(code)
        survey_steps = []

        for _, row in survey_df.iterrows():
            conversation, start_time, end_time, _, _ = row.replace({np.nan: None}).to_numpy()
            survey_conversation_step = {'type': StepType.CONVERSATION.value, 'conversation_code': conversation, 'start_time':start_time, 'end_time': end_time}
            reason_step = {'type': StepType.REASON.value, 'conversation_code': conversation, 'start_time': end_time, 'end_time': None}
            survey_steps.extend([survey_conversation_step, reason_step])

        return survey_steps
    

    def get_user_survey_by_user_code(self, code):
        file_path = settings.USERS_SURVEYS_DIR + r'\{}.xlsx'.format(code)
        survey_df = pd.read_excel(file_path)
        return survey_df