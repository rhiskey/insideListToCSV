from Classes.Detail import Detail


class CSVDoc2(Detail):
    def __init__(self, update_date):
        self.date_time = update_date
        super().__init__(self)

class CSVDoc():
    def __init__(self, name, evidence, inn, address, website, update_date):
        self.name = name
        self.evidence = evidence
        self.inn = inn
        self.address = address
        self.website = website
        self.update_date = update_date

