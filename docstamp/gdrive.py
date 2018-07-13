"""
Helpers to connect and work with google drive spreadsheets
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connect_to_gspread(google_api_key_file):
    """ Return the connection to a Google spreadsheet.

    :param google_api_key_file: path to a json file with credentials.
           Detailed here: https://developers.google.com/identity/protocols/application-default-credentials
    :type google_api_key_file: str

    :return: gspread.client.Client
    """
    scope = ["https://spreadsheets.google.com/feeds"]

    # authenticate
    credentials = ServiceAccountCredentials.from_json_keyfile_name(google_api_key_file, scope)
    return gspread.authorize(credentials)


def get_spreadsheet(api_key_file_path, doc_key):
    """
    :param api_key_file_path: path to a json file with credentials.
    :param doc_key: key of the document
    :return: gspread.models.Spreadsheet
    """
    gc = connect_to_gspread(api_key_file_path)
    if doc_key.startswith('http'):
        return gc.open_by_url(doc_key)
    else:
        return gc.open_by_key(doc_key)


def worksheet_to_dict(wks, header='', start_row=1):
    """ Transform a gspread worksheet into a pandas DataFrame.

    :param wks:
    :param header:
    :param start_row:
    :return:
    """
    all_rows = wks.get_all_values()
    if not header:
        header = all_rows[0]

    #print(list(zip(header, all_rows)))
    #[dict(zip(header, values)) for values in all_rows[1:]]
    return [dict(zip(header, values)) for values in all_rows[start_row:]]


def get_spread_url(spread_key):
    return 'https://docs.google.com/spreadsheets/d/{}'.format(spread_key)


def get_live_form_url(form_key):
    return 'https://docs.google.com/forms/d/{}/viewform'.format(form_key)


def get_edit_form_url(form_key):
    return 'https://docs.google.com/forms/d/{}/edit'.format(form_key)
