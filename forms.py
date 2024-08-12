from apiclient import discovery
from httplib2 import Http
from oauth2client.service_account import (
    ServiceAccountCredentials
)
import json
import gspread
import pandas as pd

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'finances-412021-6a2f6bed0c79.json',
    SCOPES
)


client = gspread.authorize(creds)
sheet_id = "1GWe_djvsqOYHj9a-V6ZA0q1I2uIFXsHrwv9mOSPmbPY"
sheet = client.open_by_key(sheet_id)
res_df = pd.DataFrame().from_records(sheet.sheet1.get_all_records())
print(res_df.shape)
print(res_df.columns)

emails_list = set(res_df["Dirección de correo electrónico"].to_list())
print(emails_list)


http = creds.authorize(Http())
form_service = discovery.build(
    'forms',
    'v1',
    http=http,
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False
)
form_id = "1YPWAAjRgh4n2Jq9cfRNh3xZQnZzZuqku-F6r37Ka7S8"
result = form_service.forms().get(formId=form_id).execute()
print(result)
print("Google Form obtained!")

for email_pl in emails_list:
    filtered = res_df.loc[res_df["Dirección de correo electrónico"]==email_pl]
    

    P_VALS = filtered["Nombre de la iniciativa"].to_list()


    for initiative in P_VALS:

        new_form = {
            "info": {
                "title": f"PL: {email_pl}" + f"initiative: {initiative}"
            }
        }

        form_res = form_service.forms().create(
            body=new_form
        ).execute()

        responded_uri = form_res["responderUri"]
        print(responded_uri)







# P_VALS = []
# POSSIBLE_VALUES = [{'value': p_val} for p_val in P_VALS]
# new_form = {
#     "info": result["info"],
#     "items": [
#         {
#             'itemId': '3a808847',
#             'title': 'Nombre de la iniciativa',
#             'questionItem':
#             {'question':
#                 {
#                     'questionId': '3cf06a1a',
#                     'required': True,
#                     'choiceQuestion': {
#                         'type': 'DROP_DOWN',
#                         'options': [
#                             {'value': 'Nombre A'},
#                             {'value': 'Nombre B'}
#                         ]
#                     }
#                 }
#             }
#         }
#     ],
# }

# [
#     {
#         'itemId': '3a808847',
#         'title': 'Nombre de la iniciativa',
#         'questionItem':
#         {'question':
#             {
#                 'questionId': '3cf06a1a',
#                 'required': True,
#                 'choiceQuestion': {
#                     'type': 'DROP_DOWN',
#                     'options': [
#                         {'value': 'Nombre A'},
#                         {'value': 'Nombre B'}
#                     ]
#                 }
#             }
#         }
#     }
# ]




# NEW_FORM = {
#   "info": {
#     "title": "test"
#   },
#   "items": [
#     {
#       "title": "test",
#       "description": "test",
#         "questionItem": {
#             "question": {
#                 {
#                     "required": True,
#                     "choiceQuestion": {
#                     "type": "RADIO",
#                     "options": [
#                         {
#                             "value": "A",
#                             "isOther": False,
#                             "goToAction": "GO_TO_ACTION_UNSPECIFIED"
#                         }
#                     ],
#                     "shuffle": False
#                     }

#                 },
#             },
#         },
#     }
#   ],
# }

# result = form_service.forms().create(
#     body=NEW_FORM
# ).execute()

# question_setting = form_service.forms().batchUpdate(
#     formId=result["formId"],
#     body=NEW_QUESTION
# ).execute()

# get_result = form_service.forms().get(
#     formId=result["formId"]
# ).execute()

# print(json.dumps(get_result, indent=4))

# PARENT_FOLDER_ID = "1xMuwbnCR_xRZVJHXc30WwuuY8K0wNlcG"

# FILE_PATH = "copy.txt"
# service = discovery.build(
#     "drive",
#     "v3",
#     credentials=creds
# )
# file_metadata = {
#     "name": "hello",
#     "parents": [PARENT_FOLDER_ID],
# }
# file = service.files().create(
#     body=file_metadata,
#     media_body=FILE_PATH,
# ).execute()