from Classes.Detail import Detail
import json


class CSVDoc2(Detail):
    def __init__(self, update_date):
        self.date_time = update_date
        super().__init__(self)


class CSVDoc:
    def __init__(self, id_site, name, evidence, inn, address, website, update_date):
        self.org_id = id_site
        self.name = name
        self.evidence = evidence
        self.inn = inn
        self.address = address
        self.website = website
        self.update_date = update_date


class CSVDocEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CSVDoc):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

