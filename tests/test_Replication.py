from tkinter import Tk
from unittest import TestCase
from Replication import Replication
from db_interface.DatabaseODBC import DatabaseODBC
from user_interface.UI import UI
from write_tables_csv import tables
from main import find_table
from pypyodbc import Error


class TestReplication(TestCase):
    def test_replicate_client(self):
        home = DatabaseODBC()
        home.connect("gdr")
        replication = Replication(UI(Tk(), []))
        t_name = "Client"
        try:
            replicated = replication.replicate(home, home, t_name, tables[find_table(t_name, tables)][1],
                                               "31082019")
            self.assertIs(None, replicated)
        except Error as Er:
            self.fail(Er)
