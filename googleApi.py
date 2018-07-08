from __future__ import print_function
import httplib2
<<<<<<< HEAD
import requests
import os
import json
import pprint
=======
import os
>>>>>>> d38fa26557c9d8d24a3c95e4e938a4d73c0c7188

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

<<<<<<< HEAD
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

=======
>>>>>>> d38fa26557c9d8d24a3c95e4e938a4d73c0c7188
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

<<<<<<< HEAD
# https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.html#batchUpdate

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'stockDash-604bfd160091.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def getValues(authed_session,sheetID,sheetRange):

    r = authed_session.get("https://sheets.googleapis.com/v4/spreadsheets/"+sheetID+"/values/"+sheetRange)
    data = json.loads(r.content)["values"]

    return(data)

def updateValues(authed_session,sheetID,sheetRange,sendData):

    r = authed_session.put("https://sheets.googleapis.com/v4/spreadsheets/"+sheetID+"/values/"+sheetRange+"?valueInputOption=RAW",
                           json.dumps({"values":sendData}))
    data = json.loads(r.content)

    return(data)

def header1(authed_session,SheetID,GID,Row):

    b = json.dumps(
        {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": GID,
                            "startRowIndex": Row-1,
                            "endRowIndex": Row,
                            "startColumnIndex": 0,
                            "endColumnIndex": 100
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": 0.9,
                                    "green": 0.9,
                                    "blue": 0.9,
                                },
                                "horizontalAlignment": "CENTER",
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 0.0,
                                        "green": 0.0,
                                        "blue": 0.0
                                    },
                                    "fontSize": 10,
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                    }
                },
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": GID,
                            "gridProperties": {
                                "frozenRowCount": 6
                            }
                        },
                        "fields": "gridProperties.frozenRowCount"
                    }
                }
            ]
        }
    )

    r = authed_session.post("https://sheets.googleapis.com/v4/spreadsheets/"+SheetID+":batchUpdate",b)
    data = json.loads(r.content)
    return(data)

def divider1(authed_session,SheetID,GID,Row):

    b = json.dumps(
        {
            "requests":[
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": GID,
                            "startRowIndex": Row-1,
                            "endRowIndex": Row,
                            "startColumnIndex": 0,
                            "endColumnIndex": 100
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "borders": {
                                    "bottom": {
                                        "style": "SOLID",
                                        "color": {
                                            "red": 0.0,
                                            "green": 0.0,
                                            "blue": 0.0
                                        }
                                    },
                                }
                            }
                        },
                        "fields": "userEnteredFormat(borders)"
                    }
                }
            ]
        }
    )

    r = authed_session.post("https://sheets.googleapis.com/v4/spreadsheets/"+SheetID+":batchUpdate",b)
    data = json.loads(r.content)
    return(data)

def clearLines(authed_session,SheetID,GID,Row):

    b = json.dumps(
        {
            "requests":[
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": GID,
                            "startRowIndex": Row-1,
                            "endRowIndex": Row+100,
                            "startColumnIndex": 0,
                            "endColumnIndex": 100
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "borders": {
                                    "top": {
                                        "style": "NONE",
                                        "color": {
                                            "red": 0.0,
                                            "green": 0.0,
                                            "blue": 0.0
                                        }
                                    },
                                    "bottom": {
                                        "style": "NONE",
                                        "color": {
                                            "red": 0.0,
                                            "green": 0.0,
                                            "blue": 0.0
                                        }
                                    },
                                    "left": {
                                        "style": "NONE",
                                        "color": {
                                            "red": 0.0,
                                            "green": 0.0,
                                            "blue": 0.0
                                        }
                                    },
                                    "right": {
                                        "style": "NONE",
                                        "color": {
                                            "red": 0.0,
                                            "green": 0.0,
                                            "blue": 0.0
                                        }
                                    },
                                }
                            }
                        },
                        "fields": "userEnteredFormat(borders)"
                    }
                }
            ]
        }
    )

    r = authed_session.post("https://sheets.googleapis.com/v4/spreadsheets/"+SheetID+":batchUpdate",b)
    data = json.loads(r.content)
    return(data)

def main():
    pass
=======
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'googleCred.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def updateValues(sheetID,sheetRange,sheetValues):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    service.spreadsheets().values().update(spreadsheetId=sheetID,
                                           range=sheetRange,
                                           body={"values": sheetValues},
                                           valueInputOption='RAW').execute()


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1d9Ae3G9g2be--a3tL-wvTbdZUwHluqiZu0wNKA7moQ8'
    rangeName = 'weekly wires!A1:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    #print(values)

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('{} {}'.format(row[0],row[4]))

    data = {"values": [['APIsym']]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId,
                                                range='Options!A1', body=data, valueInputOption='RAW').execute()
>>>>>>> d38fa26557c9d8d24a3c95e4e938a4d73c0c7188

if __name__ == '__main__':
    main()
