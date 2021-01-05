#https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
import mysql.connector as sql
from mysql.connector import errorcode #For checking exceptions


def seperator(newlines = 0):
    sep = '-' * 80; newlines = '\n' * newlines
    print(f'\n\n{sep}xxx{sep}{(newlines)}')



#ID and password for database
config = {'host' : "localhost",
          'user' : "root",
          'passwd' : "Gamingrowdy@13"}

db = sql.connect(**config)
csr = db.cursor()


def close():
    """ commit changes to database and close connection """

    csr.close() #Closing cursor
    db.commit() #Saves all changes
    db.close()  #Closing connection with db



def db_existance(db_name):
    """ checks if database exists """

    csr.execute('SHOW DATABASES')
    csr.fetchall()
    for _db in csr:
        if _db[0] == db_name:
            return True
    return False



def show_dbs():
    csr.execute('SHOW DATABASES')
    return csr.fetchall()[3:]



def get_connection(db_name = None):
    """ returns the connection object """

    if not db_name:
        return db

    connect_config = config
    connect_config['database'] = db_name #adding db to the config declared globally
    try:
        _db = sql.connect(**connect_config)
    except Exception as e:
        print('[Error]', e)
    else:
        return _db



def create_db(db_name, connect = False):
    """ creates a database """

    try:
        print(f'Creating DATABASE {db_name}: ', end = '')
        csr.execute(f'CREATE DATABASE {db_name}')
    except Exception as err:
        print('Error occurred')
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f'[Error] DATABASE {db_name} already exists.')
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
            print(f'[Error] DATABASE {db_name} doesn\'t exist.')
        else:
            print(err)
    else:
        print('Success')



def create_table(tb_name, data, db_name):
    """ creates the table on database """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    try:
        print(f'Creating TABLE {tb_name}: ', end = '')
        _csr.execute(f'CREATE TABLE {tb_name} ({data})')
    except Exception as err:
        print('Error occurred')
        if err.errno == errorcode.ER_BAD_TABLE_ERROR:
            print(f'[Error] TABLE {tb_name} already exists.')
        else:
            print(err)
    else:
        print('Success')



def delete_table(tb_name, db_name):
    """ deletes the given table on database """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    try:
        print(f'Dropping TABLE {tb_name} from {db_name}:', end = ' ')
        _csr.execute(f'DROP TABLE {tb_name}')
    except Exception as err:
        print('Error occurred')
        if err.errno == errorcode.ER_BAD_TABLE_ERROR:
            print(f'[Error] TABLE {tb_name} doesn\'t exist.')
        else:
            print(err)
    else:
        print('Success')



def delete_all_tables(db_name):
    _db = get_connection(db_name)
    _csr = _db.cursor()
    csr.execute('SHOW TABLES')
    tables = csr.fetchall()
    for table in tables:
        delete_table(x[0], db_name)
    print(f'\nDeleted all tables on {db_name}.')



def insert(tb_name, db_name, cols, vals):
    _db = get_connection(db_name)
    _csr = _db.cursor()
    #print(f'INSERT INTO {tb_name} ({cols}) VALUES ({vals})')
    _csr.execute(f'INSERT INTO {tb_name} ({cols}) VALUES ({vals})')
    _db.commit()
