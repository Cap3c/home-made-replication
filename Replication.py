from tkinter import END

from pypyodbc import Cursor, Connection, ProgrammingError, Error
from db_interface.DatabaseODBC import DatabaseODBC
from user_interface.UI import UI
import re
import logging


class Replication:
    def __init__(self, ui: UI):
        self.ui = ui

    def strip_sql(self, lines: str):
        """
        Strips the SQL operations in the string
        """
        lines_sep = lines.split(',')
        for i, line in enumerate(lines_sep):
            if line == r"'YYYYMMDD')":
                lines_sep.pop(i)
            # possible templates
            # to_char(Date_sortie,'YYYYMMDD')
            # cast(heure as character(5))
            try:
                lines_sep[i] = re.split(r"[, ]", line.split('(')[1])[0]
            except IndexError:
                pass
            # can probably be refactoring using a single re.split
            # with the samples it returns ['Date_sortie', "'YYYYMMDD')"] and ['heure', 'as', 'character']
            # seems to work
        return ','.join(lines_sep)

    def where_clause(self, table, lines, date):
        """
        Determinate what the where clause to select data after date is composed of
        :param table: checks if the table is arrivage, the table where we are taking the date from
        :param lines: if there is no idarrivage field in the lines of the table, there is no Where clause
        :param date: The minimum date it will select data from
        :return: Where clause
        """
        # where the table is not arrivage
        whna = f"WHERE IDArrivage IN (SELECT IDArrivage FROM Arrivage WHERE Date > {date})"
        # where it is arrivage
        wha = f"WHERE Date > {date}"
        # where clause
        whc = wha if table.lower() == 'arrivage' else whna
        # In the case where there is not IDArrivage, you selected them all
        if "idarrivage" not in lines.lower().split(','):
            whc = ""
        return whc

    def escape(self, values, strp_lines):
        sep_l = strp_lines.split(',')
        esc = []
        for i, m in enumerate(values):
            if sep_l[i].isdigit():
                esc.append(str(m))
            else:
                esc.append(f"\'{m}\'")
        return esc

    def replicate(self, home: DatabaseODBC, away: DatabaseODBC, table, lines: str, date):
        """
        Replicates the away table with its lines into the home table
        :param home: local db
        :param away: replicated db
        :param table: name of the table
        :param lines: lines containing all the sql operations
        :param date: Lower limit of the replication
        """
        # try connecting to both DBs
        try:
            home_cur = home.DB.cursor()
        except ProgrammingError as PEr:
            logging.critical(f"Home cursor instanciation failed: {PEr}")
            raise PEr
        try:
            away_cur = away.DB.cursor()
        except ProgrammingError as PEr:
            logging.critical(f"Away cursor instanciation failed: {PEr}")
            raise PEr
        # determinate where clause
        whc = self.where_clause(table, lines, date)
        # selects all IDs from the local table
        try:
            home_cur.execute(f"SELECT {lines.split(',')[0]} FROM {table} {whc}")
        except Error as Er:
            logging.error(f"Selecting the IDs from {table} failed : {Er}")
            return Er
        home_ids_fetch = home_cur.fetchall()
        home_ids = [di[0] for di in home_ids_fetch]
        logging.info(f"{len(home_ids)} {table} IDs selected successfully")
        # Selects all data from the away table
        try:
            away_cur.execute(f"SELECT {lines} FROM {table} {whc}")
        except Error as Er:
            logging.error(f"Selecting the lines from {table} failed : {Er}")
            return Er
        logging.info(f"{table} lines selected successfully")
        # Inserts the data in the local table if the id isn't the one already in
        away_fetch = away_cur.fetchall()
        no_lines = 0
        ids_present = 0
        for m_away in away_fetch:
            if m_away[0] not in home_ids:
                try:
                    strp_lines = self.strip_sql(lines)
                    # print(esc)
                    # print(','.join(esc))
                    home_cur.execute(
                        f"INSERT INTO {table}({strp_lines}) VALUES ({','.join(self.escape(m_away, strp_lines))})")
                    no_lines += 1
                except Error as Er:
                    logging.error(f"Insert into {table} failed at ID {m_away[0]} : {Er}")
            else:
                ids_present += 1
        #
        self.ui.text_tables.configure(state="normal")
        self.ui.text_tables.insert(END, f"\n{table} inserted")
        self.ui.text_tables.configure(state="disabled")
        #
        logging.info(
            f"{no_lines} lines in {table} inserted successfully over {len(home_ids)} lines, {ids_present} were "
            f"already present")

        home_cur.commit()
        home_cur.close()  # safety mesure
