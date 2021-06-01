from Classes.Detail import Detail


class CSVDoc(Detail):
    def __init__(self, update_date):
        self.date_time = update_date
        super().__init__(self)

