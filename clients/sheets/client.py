import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings

from clients.sheets.dto import ExpressMedblogerData


class SpreadsheetDiagnostyClient:
    def __init__(self):
        self.service_account_file = settings.SERVICE_ACCOUNT_FILE
        self.spreadsheet_id = settings.SPREADSHEET_ID
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = Credentials.from_service_account_file(self.service_account_file, scopes=scopes)
        self.client = gspread.authorize(credentials)

    def create_row(self, data: ExpressMedblogerData):
        sheet = self.client.open_by_key(self.spreadsheet_id).worksheet("Предзапись на всё")
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
