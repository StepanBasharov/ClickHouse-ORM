class UndefinedFieldException(Exception):
    def __init__(self, field: str):
        self.message = f"Table has not field '{field}'"
        super().__init__(self.message)

    def __str__(self):
        return self.message
