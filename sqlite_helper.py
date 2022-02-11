import sqlite3


class SqliteDb():
    def __init__(self, database: str):
        self.conn = sqlite3.connect(database)

        self.field_list_sql = """
        SELECT 
               p.name as columnName
        FROM sqlite_master m
        left outer join pragma_table_info((m.name)) p
             on m.name <> p.name
        where m. name = ?
        """

    def conn_commit(self):
        self.conn.commit()

    def conn_rollback(self):
        self.conn.rollback()

    def execute_sql(self, exec_sql, params=None):
        cur = self.conn.cursor()
        if params == None:
            cur.execute(exec_sql)
        else:
            cur.execute(exec_sql, params)
        self.conn.commit()
        return cur.lastrowid

    def execute_many_sql(self, exec_sql, lst: list):
        cur = self.conn.cursor()
        cur.executemany(exec_sql, lst)
        self.conn.commit()

    def is_table_exist(self, table_name: str) -> bool:
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        tmp = self.fetchall_records(sql, (table_name,))
        return bool(len(tmp))

    def fetchall_records(self, query_sql, params=None) -> list:
        cur = self.conn.cursor()
        if params == None:
            cur.execute(query_sql)
        else:
            cur.execute(query_sql, params)
        rows = cur.fetchall()
        return rows

    def fetchone_record(self, query_sql, params=None) -> list:
        cur = self.conn.cursor()
        if params == None:
            cur.execute(query_sql)
        else:
            cur.execute(query_sql, params)
        rows = cur.fetchone()
        return rows

    def get_insert_sql(self, table_name: str):
        lst_tmp = self.fetchall_records(self.field_list_sql, (table_name,))
        strval = 'insert into ' + table_name + '('
        fld_cnt = len(lst_tmp)
        val_tmp = ' values ('
        for fld in lst_tmp:
            strval += fld[0] + ','
            val_tmp += '?,'
        strval = strval[0:len(strval) - 1]
        val_tmp = val_tmp[0:len(val_tmp) - 1]
        strval += ')'
        val_tmp += ')'
        # print(strval + val_tmp)
        return strval + val_tmp

    def get_create_sql_from_list(self, table_name: str, columns: list) -> str:
        first_row = f'create table {table_name} ('
        total = len(columns)
        gen_sql = ''
        gen_sql += first_row
        for i, colum in enumerate(columns):
            if i + 1 != total:
                gen_sql += colum+' text ,'
            else:
                gen_sql += colum+' text );'
        return gen_sql

