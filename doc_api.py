from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1Z6UyMYIcWx81b9Lb9qvKwN4yXGvK3ff5o2TyAHn1jY4'

doc_date = '29/04'

def read_structural_elements(elements, doc_date):
    tasks = []
    found_date = False
    for value in elements:
        if 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                if not found_date: 
                    day_index = 0
                cells = row.get('tableCells')
                if not found_date:
                    for cell in cells:
                        # Find date
                        for value in cell.get('content'):
                            for element in (value.get('paragraph').get('elements')):
                                text_run = element.get('textRun')
                                if text_run:
                                    cell_text = text_run.get('content').strip()
                                    if cell_text == doc_date:
                                        found_date = True
                                        print("Found Date:", cell_text, "at index", day_index)
                                        break
                        if not found_date: 
                            day_index += 1
                else:
                    cell = cells[day_index]
                    for value in cell.get('content'):
                        for element in (value.get('paragraph').get('elements')):
                            text_run = element.get('textRun')
                            if text_run:
                                tasks.append(text_run.get('content').strip())
                    return [task for task in tasks if task != '']

    return ['Nothing scheduled for today']

    
def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
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

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        # print('The title of the document is: {}'.format(document.get('title')))

        doc_content = document.get('body').get('content')
        print(read_structural_elements(doc_content, doc_date))                
        
    except HttpError as err:
        print(err)
        


if __name__ == '__main__':
    main()
