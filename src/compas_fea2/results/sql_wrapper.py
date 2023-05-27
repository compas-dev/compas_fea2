from operator import index
import sqlite3
import sqlalchemy as db


def create_connection(db_file=None):
    """Create a database connection to the SQLite database specified by db_file.

    Parameters
    ----------
    db_file : str, optional
        Path to the .db file, by default 'None'. If not provided, the database
        is run in memory.

    Return
    ------
    :class:`sqlite3.Connection` | None
        Connection object or None
    """
    engine = db.create_engine("sqlite:///{}".format(db_file))
    connection = engine.connect()
    metadata = db.MetaData()
    return engine, connection, metadata

def get_database_table(engine, metadata, table_name):
    """Retrieve a table from the database.

    Parameters
    ----------
    engine : _type_
        _description_
    metadata : _type_
        _description_
    table_name : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return db.Table(table_name, metadata, autoload=True, autoload_with=engine)

def get_query_results(connection, table, columns, test):
    """Get the filtering query to execute.

    Parameters
    ----------
    connection : _type_
        _description_
    table : _type_
        _description_
    columns : _type_
        _description_
    test : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    query = db.select([table.columns[column] for column in columns]).where(db.and_(*test))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultProxy, ResultSet

def get_field_labels(engine, connection, metadata, field, label):
    """Get the names of the components or invariants of the field

    Parameters
    ----------
    engine : _type_
        _description_
    connection : _type_
        _description_
    metadata : _type_
        _description_
    field : _type_
        _description_
    label : _type_
        'components' or 'invariants'

    Returns
    -------
    _type_
        _description_
    """
    FIELDS = get_database_table(engine, metadata, 'fields')
    query = db.select([FIELDS.columns[label]]).where(FIELDS.columns.field == field)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultSet[0][0].split(' ')

def get_all_field_results(engine, connection, metadata, table):
    components = get_field_labels(engine, connection, metadata, str(table), 'components')
    invariants = get_field_labels(engine, connection, metadata, str(table), 'invariants')
    columns = ['part', 'position', 'key']+components+invariants
    query = db.select([table.columns[column] for column in columns])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultProxy, ResultSet

def get_field_results(engine, connection, metadata, table, test):
    components = get_field_labels(engine, connection, metadata, str(table), 'components')
    invariants = get_field_labels(engine, connection, metadata, str(table), 'invariants')
    labels = ['part', 'position', 'key']+components+invariants
    ResultProxy, ResultSet = get_query_results(connection,
                                               table,
                                               labels,
                                               test)

    return ResultProxy, (labels, ResultSet)


if __name__ == '__main__':
    import os
    from pprint import pprint
    engine, connection, metadata = create_connection(
        r'C:\Code\myRepos\swissdemo\data\q_5\output\1_0\ULS\ULS-results.db')
    # U = db.Table('U', metadata, autoload=True, autoload_with=engine)
    U = get_database_table(engine, metadata, 'U')
    # print(RF.columns.keys())
    # query = db.select([U]).where(U.columns.key == 0)
    # query = db.select([U]).where(U.columns.part.in_ == ['BLOCK_0', 'TIE_21'])
    # query = db.func.sum(RF.columns.RF3)
    # ResultProxy, ResultSet = get_query_results(connection, RF, ['RF1', 'RF2', 'RF3'], {'step': ('==', '"udl"'),
    #                                               'magnitude': ('!=', 0.)})

    sql = """
SELECT step, part, key, MIN(U3)
FROM U
WHERE step IN ('udl') AND part || '#$' || key  in ('BLOCK_8#$1', 'BLOCK_9#$3')
GROUP BY step, part;
"""
    ResultProxy = connection.execute(sql)
    ResultSet = ResultProxy.fetchall()
    pprint(ResultSet)
    # table_name = 'RF'
    # component = 'RF3'
    # # result = connection.execute(f'SELECT rowid, MIN({component}) , MAX({component}) FROM {table_name} GROUP BY rowid')
    # result = connection.execute(f'SELECT MIN({component}) , MAX({component}) FROM {table_name}')

    # min_value = None
    # max_value = None

    # for elem in result:
    #     min_value = elem[0]
    #     max_value = elem[1]

    # print('Min value : ',min_value)
    # print('Max value : ',max_value)
