from . import Database
import pypyodbc


class DatabaseODBC(Database.Database):
    def __init__(self):
        super().__init__()
        self.dsn = ""

    def connect(self, dsn):
        """
        Connects to a DSN
        :param dsn: The DSN you're accessing to
        :type dsn: str
        :return: True if the connection is successful, False if it isn't
        """
        self.dsn = dsn
        try:
            self.DB = pypyodbc.connect(f"DSN={dsn};")
            return True
        except pypyodbc.Error:
            return False

    def __repr__(self):
        return f"<DatabaseODBC;{self.dsn}>"
