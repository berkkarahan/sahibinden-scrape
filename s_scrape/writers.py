
class _RecordWriter():
    def __init__(self):
        self.empty = True
        self.storage = None
        self.initialize()

    def initialize(self):
        self._initialize()

    def write(self, record):
        if self.empty:
            self.empty = False
        self._write(record)

    def save(self, filename):
        self._save()

class ListWriter(_RecordWriter):
    def __init__(self):
        super().__init__()

    def _initialize(self):
        self.storage = list()

    def _write(self, record):
        self.listings_list.append(record)

    def _save(self, filename):
        import csv
        keys = list(self.storage[0])
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            fw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fw.writerow(keys)

            for itm in l:
                try:
                    print("--> Writing car: "+itm['Marka']+" with clsid: "+itm['clsid']+" to csv.")
                    values = list(itm.values())
                    fw.writerow(values)
                except TypeError:
                    continue

class FrameWriter(_RecordWriter):
    def __init__(self, headings):
        super().__init__()
        self.headings = headings

    def _initialize(self):
        import pandas as pd
        self.storage = pd.DataFrame()

    def _write(self, record):
        record_dict = {}
        for k, v in zip(record, self.headings):
            record_dict[k] = v
        self.storage.append(record_dict, ignore_index = True)

    def _save(self, filename):
        self.storage.to_csv(filename, index=False)

class DatabaseWriter(_RecordWriter):
    # NYI
    pass
