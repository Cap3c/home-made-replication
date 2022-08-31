from pypyodbc import Cursor, Connection, ProgrammingError, Error
from db_interface.DatabaseODBC import DatabaseODBC
import re
import logging


class Replication:
    def __init__(self):
        pass

    def strip_sql(self, lines: str):
        lines_sep = lines.split(',')
        for i, line in enumerate(lines_sep):
            # possible templates
            # to_char(Date_sortie,'YYYYMMDD')
            # cast(heure as character(5))
            lines_sep[i] = re.split(r"[, ]", line.split('(')[1])[0]
            # with the samples it returns ['Date_sortie', "'YYYYMMDD')"] and ['heure', 'as', 'character']
            # seems to work
        return ','.join(lines_sep)

    def replicate(self, home: DatabaseODBC, away: DatabaseODBC, table, lines: str, date):
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
        # where the table is not arrivage
        whna = f"WHERE IDArrivage IN (SELECT IDArrivage FROM Arrivage WHERE Date > {date})"
        # where it is arrivage
        wha = f"WHERE Date > {date}"
        # where clause
        whc = wha if table.lower() == 'arrivage' else whna
        # In the case where there is not IDArrivage, you selected them all
        if "idarrivage" not in lines.lower().split(','):
            whc = ""

        try:
            home_cur.execute(f"SELECT {lines.split(',')[0]} FROM {table} {whc}")
        except Error as Er:
            logging.error(f"Selecting the IDs from {table} failed : {Er}")
            raise Er
        logging.info(f"{table} IDs selected successfully")

        home_ids_fetch = home_cur.fetchall()
        home_ids = [di[0] for di in home_ids_fetch]
        try:
            away_cur.execute(f"SELECT {lines} FROM {table} {whc}")
        except Error as Er:
            logging.error(f"Selecting the lines from {table} failed : {Er}")
            raise Er
        logging.info(f"{table} lines selected successfully")

        away_fetch = away_cur.fetchall()
        for m_away in away_fetch:
            if m_away[0] not in home_ids:
                try:
                    home_cur.execute(f"INSERT INTO {table}({self.strip_sql(lines)}) VALUES ({','.join(m_away)})")
                except Error as Er:
                    logging.error(f"Insert into {table} failed at ID {m_away[0]} : {Er}")
                    raise Er
        logging.info(f"All {table} inserted successfully")

        home_cur.commit()
        home_cur.close()
