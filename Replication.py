from pypyodbc import Cursor, Connection
import re


class Replication:
    def __init__(self, home_db: Connection, away_db: Connection):
        self.home_db = home_db
        self.away_db = away_db

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

    def replicate(self, table, lines, date):
        home_cur = self.home_db.cursor()
        away_cur = self.away_db.cursor()
        # where the table is not arrivage
        whna = f"WHERE idarrivage in (SELECT idarrivage from arrivage where date > {date})"
        # where it is arrivage
        wha = f"WHERE date > {date}"
        # where clause
        whc = wha if table.lower() == 'arrivage' else whna
        home_cur.execute(f"SELECT {lines.split(',')[0]} FROM {table} {whc}")
        home_ids_fetch = home_cur.fetchall()
        home_ids = [di[0] for di in home_ids_fetch]
        away_cur.execute(f"SELECT {lines} FROM {table} {whc}")
        away_fetch = away_cur.fetchall()
        for m_away in away_fetch:
            if m_away[0] not in home_ids:
                home_cur.execute(f"INSERT INTO {table}({self.strip_sql(lines)}) VALUES ({','.join(m_away)})")
        home_cur.commit()
