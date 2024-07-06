class Model:
    __table__ = None

    def _get_table(self):
        return getattr(self, '__table__')
