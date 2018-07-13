import sys

from .unicode_csv import UnicodeWriter

if sys.version_info[0] >= 3:
    raw_input = input


class GoogleData:

    def getCSV(self):
        """
        Returns
        -------
        filename: str
        """
        import getpass
        import gspread

        user = raw_input("Insert Google username:")
        password = getpass.getpass(prompt="Insert password:")
        name = raw_input("SpreadSheet filename on Drive:")
        sheet = raw_input("Sheet name (first sheet is default):")

        cl = gspread.login(user, password)
        sh = cl.open(name)

        if not (sheet.strip()):
            ws = sh.sheet1
            sheet = "1"
        else:
            ws = sh.worksheet(sheet)

        filename = name + '-worksheet_' + sheet + '.csv'
        with open(filename, 'wb') as f:
            writer = UnicodeWriter(f)
            writer.writerows(ws.get_all_values())

        return filename
