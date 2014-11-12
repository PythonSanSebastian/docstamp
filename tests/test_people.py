# -*- coding: utf-8 -*-


class TestCSV():

    def test_csv_loading(self):
        pass

if __name__ == '__main__':
    #script for testing/development purpose
    import os
    import csv
    import json
    from pydger.people import ConferenceParticipant, Participants

    csvf = os.path.join(os.path.dirname(__file__), '..', '..', 'registrations.csv')
    people = Participants()

    with open(str(csvf), 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            part = ConferenceParticipant.from_json_str(json.dumps(row))
            if not part.is_empty:
                people.add(part)
                print(part)

