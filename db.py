import mysql.connector as sql
from mysql.connector import errorcode #For checking exceptions
from data import *

def seperator(n1 : int = 0, n2 : int = 0):
    """ line seperator to decorate terminal """

    n1, n2 = '\n' * n1, '\n' * n2
    print(f'{n1}{sep}xxx{sep}{n2}') #sep (seperator) from data.py



db = sql.connect(**config)
csr = db.cursor()



def db_existance(db_name):
    """ checks if database exists """

    if db_name.lower() in show_dbs():
            return True
    return False



def show_dbs():
    """ return all the existing dbs except the 3 main schemas """

    csr.execute('SHOW DATABASES')
    return [x[0] for x in csr.fetchall()[3:]]



def get_connection(db_name = None):
    """ returns the connection object """

    if not db_name:
        return db

    config_copy = config
    config_copy['database'] = db_name #adding db to the config declared globally
    try:
        _db = sql.connect(**config_copy)
    except Exception as e:
        print('\t[Error]', e)
    else:
        return _db



def create_db(db_name : str, connect : bool = False):
    """ creates a database """

    try:
        print(f'Creating DATABASE {db_name}: ', end = '')
        csr.execute(f'CREATE DATABASE {db_name}')
    except Exception as err:
        print('Error occurred')
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f'\t[Error] DATABASE {db_name} already exists.')
        else:
            print(err)
    else:
        print('Success')

    #Returns the connection obbject if requested while calling this function
    if connect:
        return get_connection(db_name)



def delete_db(db_name):
    """ delete given database """

    try:
        print(f'Dropping DATABASE {db_name}:', end = ' ')
        csr.execute(f'DROP DATABASE {db_name}')
    except sql.Error as err:
        print('Error occurred!')
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f'\t[Error] DATABASE {db_name} doesn\'t exist.')
        else:
            print('\t[Error] ', err)
    else:
        print('Success')



def delete_all_dbs():
    """ delete all database """

    for db_name in show_dbs():
        delete_db(db_name)
    print("\nDeleted all databases!")



def create_table(tb_name, data, db_name):
    """ creates the table on database """

    _db = get_connection(db_name)
    try:
        print(f'Creating TABLE {tb_name}: ', end = '')
        _db.cursor().execute(f'CREATE TABLE {tb_name} ({data})')
    except Exception as err:
        print('Error occurred')
        if err.errno == errorcode.ER_BAD_TABLE_ERROR:
            print(f'\t[Error] TABLE {tb_name} already exists.')
        else:
            print('\t[Error] ', err)
    else:
        print('Success')



def delete_table(tb_name, db_name):
    """ deletes the given table on database """

    _db = get_connection(db_name)
    try:
        print(f'Dropping TABLE {tb_name} from {db_name}:', end = ' ')
        _db.cursor().execute(f'DROP TABLE {tb_name}')
    except Exception as err:
        print('Error occurred')
        if err.errno == errorcode.ER_BAD_TABLE_ERROR:
            print(f'\t[Error] TABLE {tb_name} doesn\'t exist.')
        else:
            print('\t[Error] ', err)
    else:
        print('Success')



def delete_all_tables(db_name):
    """ deletes all tables in a given database """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute('SHOW TABLES')
    tables = _csr.fetchall()
    for table in tables:
        delete_table(x[0], db_name)
    print(f'\nDeleted all tables on {db_name}.')



def get_all_tables(db_name):
    """ returns all tables from a database """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SHOW TABLES')

    return [x[0] for x in _csr.fetchall()]



def insert(tb_name, db_name, cols, vals):
    """ inserts value into the table requires all the 4 parameters are mandatory """

    _db = get_connection(db_name)
    #print(f'INSERT INTO {tb_name} ({cols}) VALUES ({vals})')
    _db.cursor().execute(f'INSERT INTO {tb_name} ({cols}) VALUES ({vals})')
    _db.commit()



def delete_row(tb_name, db_name, condition):
    """ deletes a row from table which satisfies the condition """

    _db = get_connection(db_name)
    #print(f'DELETE FROM {tb_name} WHERE {condition}')
    _db.cursor().execute(f'DELETE FROM {tb_name} WHERE {condition}')
    _db.commit()




def fetch(tb_name, db_name, cols = '*', condition = ''):
    """ basic select query """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT {cols} FROM {tb_name} {condition}')

    return _csr.fetchall()
