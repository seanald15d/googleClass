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


def create_remote_document(drive_service, document_name, folder_id, parent_id=None):
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='" + parent_id + "'",
                                         pageSize=10).execute()
    items = results.get("files", [])

    print(items)

    parents = []
    final_loc = []
    for item in items:
        parents.append(drive_service.files().get(fileId=item['id'],
                                                 fields='parents').execute())
        for parent in parents:
            potential = (drive_service.files().get(fileId=parent["parents"][0]).execute())
            if potential["name"] == "Project 2":
                final_loc.append(item)

    print(final_loc)

    if items[1]['name'] == parent_id:
        parent_folder = items[1]

    # update document on drive
    file_id = '1Y2ChcMRcNjCOysiRkTmdCS8TmVUtcd1ZpQ9lNj849Eo'
    file = drive_service.files().update(fileId=file_id,
                                        addParents=final_loc[0]['id'],
                                        fields='id, parents').execute()
    '''
    title = document_name
    print(title)
    body = {
        "title": title,
        'mimeType': "application/vnd.google-apps.document"
    }

    if parent_id is not None:
        try:
            body['parents'] = [final_loc[0]['id']]
        except UnboundLocalError:
            print("moving on")
    '''
    # drive_service.files().create(body=body).execute()


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

    # before execute, need to check that folder returns what we want
    # drive_service.files().create(body=body).execute()


def make_docs(cl):
    for name in cl:
        create_remote_document(drive_service=s, document_name=f"{name}_project2_brainstorming",
                               folder_id=i, parent_id=name)


def make_folders(cl):
    for name in cl:
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 1")
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 2")
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 3")
        create_remote_folder(drive_service=s, folder_name=name, folder_items=i, parent_id="Project 4")


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
    results = service.files().list(pageSize=1000, fields='nextPageToken, files(id, name)').execute()
    desired_folder = "Project 2"

    items = results.get('files', [])

    wanted_list = []

    for item in items:
        if item['name'] == desired_folder:
            wanted_list.append(item)

    return service, wanted_list


if __name__ == '__main__':
    s, i = main()

    class_list = read_class(file_string="class.txt")

    # make_folders(class_list)
    make_docs(class_list)
