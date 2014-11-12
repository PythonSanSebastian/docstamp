
import getpass
import gspread
from .unicode_csv import UnicodeWriter

class Google_data:

    def getCSV(self):
        #returns filename
        user = raw_input("insert google username:")
        password = getpass.getpass(prompt="insert password:")
        name = raw_input("spreadsheet name:")
        sheet = raw_input("sheet name (default sheet 1):")

        cl = gspread.login(user, password)
        sh = cl.open(name)

        if not(sheet.strip()):
            ws = sh.sheet1
            sheet = "1"
        else:
            ws = sh.worksheet(sheet)

        filename = name + '-worksheet' + sheet + '.csv'
        with open(filename, 'wb') as f:
            writer = UnicodeWriter(f)
            writer.writerows(ws.get_all_values())
        return(f)
