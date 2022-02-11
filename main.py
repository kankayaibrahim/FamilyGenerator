# python3
import os
import random
from uuid import uuid4
from sqlite_helper import SqliteDb
import hashlib
from blood_group import get_random_bload_group
from randomtest import get_female_random_height, get_female_random_weight, get_male_random_height, get_male_random_weight

def get_md5_from_string(strval: str) -> str:
    md5str = hashlib.md5(strval.encode("utf")).hexdigest()
    return md5str




def get_random_female_name(conn, diff_name: str = None):
    if not diff_name:
        sql = "select name from names i where i.gender = 'Kız'  ORDER BY random() limit 1"
    else:
        sql = "select name from names i where i.gender = 'Kız' and name <> '{diff_name}' ORDER BY random() limit 1"
    return conn.fetchone_record(sql)[0]


def get_random_male_name(conn, diff_name: str = None):
    if not diff_name:
        sql = "select name from names i where i.gender = 'Erkek' ORDER BY random() limit 1"
    else:
        sql = f"select name from names i where i.gender = 'Erkek' and name <> '{diff_name}'  ORDER BY random() limit 1"
    return conn.fetchone_record(sql)[0]


def get_random_surname(conn):
    sql = "select surname from surnames s ORDER BY random() limit 1"
    return conn.fetchone_record(sql)[0]

class Person():
    def __init__(self) -> None:
        self.name = ''
        self.surname = ''
        self.old = 0
        self.child_cnt = 0
        self.gender = ''
        self.familyrole = ''
        self.blood_group = ''
        self.weight = 0
        self.height = 0
        self.hash_info = ''



def save_to_sqlite(conn, p:Person):
    # ins_sql = conn.get_insert_sql('persons')
    inssql = 'insert into persons(tckn,family_id,name,surname,gender,age_info,familyrole,blood_group,weight,height)' \
             ' values (?,?,?,?,?,?,?,?,?,?) '
    tpl = ('',p.hash_info,p.name,p.surname,p.gender,p.old, p.familyrole,p.blood_group,p.weight,p.height)
    conn.execute_sql(inssql,tpl)


class Father(Person):
    def __init__(self,conn) -> None:
        self.conn = conn
        self.name = get_random_male_name(conn)
        self.surname = get_random_surname(conn)
        self.hash_info = str(uuid4())
        self.old = random.randrange(45, 56)
        self.child_cnt = random.randrange(1, 7)
        self.wife = Wife(conn,self)
        self.grandfather = GrandFather(conn,self)
        self.grandmother = GrandMother(conn,self)
        self.gender = 'M'
        self.childs = list()
        self.familyrole = 'Father'
        self.blood_group = get_random_bload_group()
        self.weight = get_male_random_weight()
        self.height = get_male_random_height()
        

        for _ in range(self.child_cnt):
            child = Child(conn, self, random.choice(['F', 'M']))
            self.childs.append(child)
            # print(child)

    def save_to_db(self):
        save_to_sqlite(self.conn,self)
        save_to_sqlite(self.conn,self.wife)
        save_to_sqlite(self.conn, self.grandfather)
        save_to_sqlite(self.conn, self.grandmother)
        for ch in self.childs:
            save_to_sqlite(self.conn,ch) 



        

        
    def __str__(self) -> str:
        info = \
f"""
{self.surname} FAMILY
Name : {self.name}  {self.surname}
Old : {self.old}

Wife : {self.wife.name}
Wife Old: {self.wife.old}

Grand Father : {self.grandfather.name}
Grand Father Old : {self.grandfather.old}

Grand Mother : {self.grandmother.name}
Grand Mother Old : {self.grandmother.old}

Childs 
"""
        for ch in self.childs:
            info += f'Adı : {ch.name} Yaşı: {ch.old} Cinsiyet: {ch.gender} \n'
        return info

    def __repr__(self) -> str:
        return self.__str__
    


class Wife(Person):
    def __init__(self, conn, father: Father) -> None:
        self.surname = father.surname
        self.name = get_random_female_name(conn,None)
        self.old = random.randrange(father.old-10, father.old + 5)
        self.gender = 'F'
        self.familyrole = 'Wife'
        self.blood_group = get_random_bload_group()
        self.weight = get_female_random_weight()
        self.height = get_female_random_height()
        self.hash_info = father.hash_info


class GrandFather(Person):
    def __init__(self,conn, father: Father,) -> None:
        self.surname = father.surname
        self.name = get_random_male_name(conn,father.name)
        self.old = random.randrange(father.old+18, father.old + 27)
        self.gender = 'M'
        self.familyrole = 'GrandFather'
        self.blood_group = get_random_bload_group()
        self.weight = get_male_random_weight()
        self.height = get_male_random_height()
        self.hash_info = father.hash_info


class GrandMother(Person):
    def __init__(self, conn, father: Father) -> None:
        self.surname = father.surname
        self.name = get_random_female_name(conn,father.wife.name)
        self.old = random.randrange(father.old+18, father.old + 27)
        self.gender = 'F'
        self.familyrole = 'GrandMother'
        self.blood_group = get_random_bload_group()
        self.weight = get_female_random_weight()
        self.height = get_female_random_height()
        self.hash_info = father.hash_info


class Child(Person):
    def __init__(self, conn, father: Father, gender: str) -> None:
        self.surname = father.surname
        self.gender = gender
        tmp_names = []
        if len(father.childs) > 0:
            for ch in father.childs:
                tmp_names.append(ch.name)

        if self.gender == 'F':
            self.name = get_random_female_name(conn,father.wife.name)
            while self.name in tmp_names: 
                self.name = get_random_female_name(conn,father.wife.name)
        else:
            self.name = get_random_male_name(conn, father.name) 
            while self.name in tmp_names: 
                self.name = get_random_male_name(conn, father.name)

        self.old = random.randrange(10, father.old - 18)
        self.blood_group = get_random_bload_group()
        self.familyrole = 'Child'
        self.blood_group = get_random_bload_group()
        if self.gender == 'F':
            self.weight = get_female_random_weight()
            self.height = get_female_random_height()
        else:
            self.weight = get_male_random_weight()
            self.height = get_male_random_height()
        self.hash_info = father.hash_info

        

    def __str__(self) -> str:
        return f'Adı : {self.name} Yaşı: {self.old} Cinsiyet: {self.gender} '

    def __repr__(self) -> str:
        return f'Adı : {self.name} Yaşı: {self.old} Cinsiyet: {self.gender} '







def main():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    conn = SqliteDb(BASEDIR+os.sep+'isim_soyisim.sqlite')
    total = 10_000
    for i in range(total+1):
        bb = Father(conn)
        bb.save_to_db()
        print(f'\r {i} / {total} ',end='')

if __name__ == '__main__':
    main()
