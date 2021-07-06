#To avoid the confusions of the existing tools
from __future__ import print_function
#It checks whether the path is exists or not
import os.path
#It prints data neat and cleanly
import pprint
#In order to build the client libraries
from googleapiclient.discovery import build
#In order to handle entire flow we import installed app flow
from google_auth_oauthlib.flow import InstalledAppFlow
#Manually refreshing the credentials
from google.auth.transport.requests import Request
#To provide the oauth2 access and refresh tokens
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES=['https://mail.google.com/']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_email_list():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    return results.get('messages', [])

def get_email_content(message_id):
    service = get_gmail_service()
    user_data = service.users().messages().get(userId='me', id=message_id).execute()
    return user_data

def email_content_trash(message_id):
    service = get_gmail_service()
    user_data = service.users().messages().trash(userId='me', id=message_id).execute()
    return user_data

def email_content_delete(message_id):
    service = get_gmail_service()
    user_data = service.users().messages().delete(userId='me', id=message_id).execute()
    return user_data

def email_content_untrash(message_id):
    service = get_gmail_service()
    user_data = service.users().messages().untrash(userId='me', id=message_id).execute()
    return user_data

def email_batch_modify(message_id):
    string={"ids":[message_id],
    "removeLabelIds":["CATEGORY_UPDATES"]}
    service=get_gmail_service()
    user_data = service.users().messages().batchModify(userId='me', body=string).execute()
    print("batchmodify successfull")
    return user_data

if __name__ == '__main__':
    #messages = get_emails_list()
    #for message in messages:
        #print(message['id'])
    print(get_email_list())
    #id=input("enter id:")
    print(email_batch_modify('179b8b454589d9a4'))
    #print(email_content_delete('179ac38495cc5c45'))
    #print(email_content_trash('17968de923c3e73d'))
    #print(email_content_untrash('17968de923c3e73d'))