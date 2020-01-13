import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def read_class(file_string):
    with open(file_string, 'r') as f1:
        c_list = f1.readlines()
        c_list = [elem.strip("\n") for elem in c_list]
    return c_list


def create_remote_folder(drive_service, folder_name, folder_items, parent_id=None):
    # find folder by parent name
    for item in folder_items:
        if item['name'] == parent_id:
            parent_folder = item
    # Create a folder on Drive, returns the newely created folders ID
    body = {
        'name': folder_name,
        'mimeType': "application/vnd.google-apps.folder"
    }
    if parent_id:
        body['parents'] = [parent_folder['id']]
    drive_service.files().create(body=body).execute()


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')

    return service, items


if __name__ == '__main__':
    s, i = main()

    class_list = read_class(file_string="class.txt")
    for name in class_list:
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 1")
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 2")
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 3")
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 4")
