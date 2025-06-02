from __future__ import annotations

import codecs
import csv
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from csv import Dialect


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(
        self,
        file: StringIO,
        dialect: Dialect = csv.excel,
        encoding: str = "utf-8",
        **kwargs,
    ):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwargs)
        self.stream = file
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row: list[str]):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows: list[list[str]]):
        for row in rows:
            self.writerow(row)
