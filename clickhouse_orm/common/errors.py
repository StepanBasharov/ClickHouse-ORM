class UndefinedFieldException(Exception):
    def __init__(self):
        self.message = "Error: There are no passed fields in the table"
        super().__init__(self.message)

    def __str__(self):
        return self.message
