from __future__ import print_function
import httplib2
import requests
import os
import json
import pprint

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.html#batchUpdate

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'inputs\\stockDash-604bfd160091.json'
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

if __name__ == '__main__':
    main()
