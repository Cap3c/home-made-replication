from unittest import TestCase
from Replication import Replication
from db_interface.DatabaseODBC import DatabaseODBC
from write_tables_csv import tables
from main import find_table
from pypyodbc import Error


class TestReplication(TestCase):
    def test_replicate(self):
        home = DatabaseODBC()
        home.connect("gdr")
        replication = Replication()
        try:
            replication.replicate(home, home, "Client", tables[find_table("Client", tables)][1], "31082019")
            self.assertEqual(1, 1)
        except Error as Er:
            self.fail(Er)
