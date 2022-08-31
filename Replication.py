from pypyodbc import Cursor, Connection, ProgrammingError
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

    def replicate(self, home_db: Connection, away_db: Connection, table, lines, date):
        try:
            home_cur = home_db.cursor()
        except ProgrammingError as PEr:
            logging.critical(f"Home cursor instanciation failed: {PEr}")
            raise PEr
        try:
            away_cur = away_db.cursor()
        except ProgrammingError as PEr:
            logging.critical(f"Away cursor instanciation failed: {PEr}")
            raise PEr
        # where the table is not arrivage
        whna = f"WHERE idarrivage in (SELECT idarrivage from arrivage where date > {date})"
        # where it is arrivage
        wha = f"WHERE date > {date}"
        # where clause
        whc = wha if table.lower() == 'arrivage' else whna
        print(lines.split(',')[0])
        home_cur.execute(f"SELECT {lines.split(',')[0]} FROM {table} {whc}")
        home_ids_fetch = home_cur.fetchall()
        home_ids = [di[0] for di in home_ids_fetch]
        away_cur.execute(f"SELECT {lines} FROM {table} {whc}")
        away_fetch = away_cur.fetchall()
        for m_away in away_fetch:
            if m_away[0] not in home_ids:
                home_cur.execute(f"INSERT INTO {table}({self.strip_sql(lines)}) VALUES ({','.join(m_away)})")
        home_cur.commit()
