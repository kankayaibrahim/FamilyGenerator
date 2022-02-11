import os
from typing import Union
import psycopg2
from sqlite_helper import SqliteDb


class PgSqlDB(object):
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 5432,
                 database: str = 'postgres',
                 user: str = 'postgres',
                 password: str = 'postgres',
                 autocommit=True):
                 
        self.conn = psycopg2.connect(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     database=database)

        self.conn.autocommit = autocommit
        self.conn.set_session(autocommit=autocommit)
        self.version_sql = 'SELECT version();'

        self.field_exist_sql = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name=%s and column_name=%s;
        """

        self.field_list_sql = """
            SELECT column_name 
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name   = %s ;
        """

    def close(self):
        self.conn.close()

    def execute_sql(self, qry: str, params: tuple = None, return_last_row=False) -> Union[None, int]:
        curs = self.conn.cursor()
        curs.execute(qry, (params if params is not None else None))
        if return_last_row:
            return curs.fetchone()[0]
        else:
            return None
        curs.close()

    def execute_manny(self, qry: str, lst: list = None):
        curs = self.conn.cursor()
        curs.executemany(qry, (lst if lst is not None else None))

    def fetchone_record(self, qry: str, params: tuple = None):
        curs = self.conn.cursor()
        curs.execute(qry, (params if params is not None else None))
        result = curs.fetchone()
        curs.close()
        return result

    def fetchone_record_to_dict(self, qry: str, params: tuple = None) -> dict:
        curs = self.conn.cursor()
        curs.execute(qry, (params if params is not None else None))
        columns = [column[0] for column in curs.description]
        results = []
        for row in curs.fetchall():
            results.append(dict(zip(columns, row)))
        curs.close()
        return results[0]

    def fetchall_records(self, qry: str, params: tuple = None) -> list:
        curs = self.conn.cursor()
        curs.execute(qry, (params if params is not None else None))
        result = curs.fetchall()
        # print(curs.description)
        curs.close()
        return result

    def fetchall_records_to_dict(self, qry: str, params: tuple = None):
        curs = self.conn.cursor()
        curs.execute(qry, (params if params is not None else None))
        columns = [column[0] for column in curs.description]
        results = []
        for row in curs.fetchall():
            results.append(dict(zip(columns, row)))
        curs.close()
        return results

    def get_column_list(self, qry: str, params: tuple = None):
        curs = self.conn.cursor()
        curs.execute(qry, (params if params is not None else None))
        columns = [column[0] for column in curs.description]
        return columns

    def get_table_rec_count(self, table_name: str) -> int:
        qry = 'select count(0) from  ' + table_name
        return int(self.fetchone_record(qry=qry)[0])

    def table_exist(self, table_name: str) -> bool:
        qry = f"""
               SELECT to_regclass('public.{table_name}');
                """
        return bool(self.fetchone_record(qry)[0])

    def backup_tables_to_sqlite(self, backup_table_list: list, save_folder: str):
        for table in backup_table_list:
            column_list = self.get_column_list(f'select * from {table} ', None)
            sqlite_conn = SqliteDb(save_folder + os.sep + table + '.sqlite')
            sqllite_create_sql = sqlite_conn.get_create_sql_from_list(table, column_list)
            sqlite_conn.execute_sql(sqllite_create_sql)
            get_insql = sqlite_conn.get_insert_sql(table)
            data_list = self.fetchall_records(f'select * from {table}')
            sqlite_conn.execute_many_sql(get_insql, data_list)
            print('tüm kayıtlar aktarıldı ', table)

    def field_exist(self, table_name: str, field_name: str) -> bool:
        control = self.fetchone_record(self.field_exist_sql, (table_name, field_name))
        if control is None:
            return False
        else:
            return True
        # return bool(self.fetchone_record(self.field_exist_sql, (table_name, field_name))[0])

    def get_insert_sql(self, table_name: str) -> str:
        lst_tmp = self.fetchall_records(self.field_list_sql, (table_name,))
        strval = 'insert into ' + table_name + '('
        fld_cnt = len(lst_tmp)
        val_tmp = ' values ('
        for fld in lst_tmp:
            strval += fld[0] + ','
            val_tmp += '%s,'
        strval = strval[0:len(strval) - 1]
        val_tmp = val_tmp[0:len(val_tmp) - 1]
        strval += ')'
        val_tmp += ')'
        # print(strval + val_tmp)
        return strval + val_tmp

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
