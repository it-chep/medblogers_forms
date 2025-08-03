import datetime

import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings

from clients.sheets.dto import ExpressMedblogerData, NeuroMedblogerData, SmmSpecialistData


class SpreadsheetClient:
    def __init__(self, ):
        self.service_account_file = settings.SERVICE_ACCOUNT_FILE
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = Credentials.from_service_account_file(self.service_account_file, scopes=scopes)
        self.client = gspread.authorize(credentials)
        self._init_spreadsheets_id()

    def _init_spreadsheets_id(self):
        self.diagnosty_speadsheet_id = settings.SPREADSHEET_DIAGNOSTY_ID
        self.neuro_speadsheet_id = settings.SPREADSHEET_NEURO_ID
        self.smm_spreadsheet_id = settings.SPREADSHEET_SMM_ID

    def create_diagnosty_row(self, data: ExpressMedblogerData):
        sheet = self.client.open_by_key(self.diagnosty_speadsheet_id).worksheet("Предзапись на всё")
        sheet.append_row(
            [
                f'{data.name}', f'{data.phone}', f'{data.email}', f'{data.instagram_username}',
                f'{data.tg_channel_url}', f'{data.tg_username}', f'{data.marketing_type}',
                f'{data.have_bought_products}', f'{data.speciality}', f'{data.age}', f'{data.city}',
                f'{data.average_income}', f'{data.medblog}', f'{data.medblog_reason}', f'{data.medblog_complexity}',
                f'{data.medblog_helped}', f'{data.how_long_following}', f'{data.top_questions}',
                f'{data.how_warmed_up}', f'{data.rate_of_employment}',
            ]
        )

    def create_neuro_row(self, data: NeuroMedblogerData):
        sheet = self.client.open_by_key(self.neuro_speadsheet_id).worksheet("Предзапись")
        sheet.append_row(
            [
                f'{data.name}', f'{data.phone}', f'{data.email}', f'{data.tg_username}', f'{data.speciality}',
                f'{data.city}', f'{data.level_of_use_neuro}', f'{data.your_questions}'
            ]
        )

    def create_smm_row(self, data: SmmSpecialistData):
        sheet = self.client.open_by_key(self.smm_spreadsheet_id).worksheet("АНКЕТА СММ специалисты")
        sheet.append_row(
            [
                f'{datetime.datetime.now().strftime("%d.%m.%Y")}', f'{data.user_contact}', f'{data.specialization}',
                f'{data.social_networks}', f'{data.your_experience}', f'{data.last_collaboration_period}',
                f'{data.satisfied_of_results}', f'{data.positive_specialist_contact}',
                f'{data.negative_specialist_contact}'
            ]
        )
