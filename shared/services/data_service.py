import pandas as pd
import numpy as np

from django.conf import settings
from shared.models import StepType


class DataService():

    all_users_columns = ['first_name', 'last_name', 'email','timestamp', 'code', 'survey_done']
    user_survey_columns = ['conversation', 'start_time', 'end_time', 'rating', 'reason']

    def get_conversations(self):
        conversations_df = pd.read_excel(settings.CONVERSATIONS_PATH)
        return conversations_df['code'].to_numpy()
    
    def get_human_conversations(self):
        conversations_df = pd.read_excel(settings.CONVERSATIONS_PATH)
        return conversations_df.loc[conversations_df['class'] == 1]['code'].to_numpy()

    def get_machine_conversations(selft):
        conversations_df = pd.read_excel(settings.CONVERSATIONS_PATH)
        return conversations_df.loc[conversations_df['class'] == 4]['code'].to_numpy()
    
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
                'timestamp': user[2], 'code': user[4], 'survey_done': user[5]}


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

        for ind, row in survey_df.iterrows():
            conversation, start_time, end_time, _, _ = row.replace({np.nan: None}).to_numpy()
            survey_conversation_step = {'type': StepType.CONVERSATION.value, 'conversation_code': conversation, 'start_time':start_time, 'end_time': end_time}
            reason_step = {'type': StepType.REASON.value, 'conversation_code': conversation, 'start_time': end_time, 'end_time': None}
            reason_step['end_time'] = self.get_next_conversation_start_time(survey_df, ind)
            survey_steps.extend([survey_conversation_step, reason_step])

        return survey_steps
    
    def get_next_conversation_start_time(self, survey_df, ind):
        if ind + 1 >= survey_df.shape[0]:
            return None
        return survey_df.loc[ind + 1].replace({np.nan: None})['start_time']

    def get_user_survey_by_user_code(self, code):
        file_path = settings.USERS_SURVEYS_DIR + r'\{}.xlsx'.format(code)
        survey_df = pd.read_excel(file_path)
        return survey_df
    
    def start_survey(self, timestamp, user_code, conversation_end_timestamp):
        survey_df = self.get_user_survey_by_user_code(user_code)
        survey_df.at[0, 'start_time'] = timestamp
        survey_df.at[0, 'end_time'] = conversation_end_timestamp
        self.update_user_survey(survey_df, user_code)


    def rate_conversation(self, data):
        conversation_code, end_time, rating, user_code = data
        survey_df = self.get_user_survey_by_user_code(user_code)
        survey_df.loc[survey_df['conversation'] == conversation_code, 'end_time'] = end_time
        survey_df.loc[survey_df['conversation'] == conversation_code, 'rating'] = rating
        self.update_user_survey(survey_df, user_code)

    def update_user_survey(self, survey_df, user_code):
        file_path = settings.USERS_SURVEYS_DIR + r'\{}.xlsx'.format(user_code)
        survey_df.to_excel(file_path, engine='xlsxwriter', columns=self.user_survey_columns, index=False)

    def give_reason(self, data):
        conversation_code, user_code, reason, conversation_start_time, conversation_end_time, started_conversation_code = data
        survey_df = self.get_user_survey_by_user_code(user_code)
        survey_df.loc[survey_df['conversation'] == conversation_code, 'reason'] = reason
        if started_conversation_code:
            survey_df.loc[survey_df['conversation'] == started_conversation_code, 'start_time'] = conversation_start_time
            survey_df.loc[survey_df['conversation'] == started_conversation_code, 'end_time'] = conversation_end_time
        self.update_user_survey(survey_df, user_code)


    def end_user_survey(self, code):
        users_df = pd.read_excel(settings.USERS_PATH)
        users_df.loc[users_df['code'] == code, 'survey_done'] = True
        users_df.to_excel(settings.USERS_PATH, engine='xlsxwriter', columns=self.all_users_columns, index=False)


    def reset_user_survey(self, code):
        users_df = pd.read_excel(settings.USERS_PATH)
        users_df.loc[users_df['code'] == code, 'survey_done'] = False
        users_df.to_excel(settings.USERS_PATH, engine='xlsxwriter', columns=self.all_users_columns, index=False)
        survey_df = self.get_user_survey_by_user_code(code)
        for ind, row in survey_df.iterrows():
            survey_df.at[ind, 'start_time'] = None
            survey_df.at[ind, 'end_time'] = None
            survey_df.at[ind, 'rating'] = None
            survey_df.at[ind, 'reason'] = None
        self.update_user_survey(survey_df, code)
