def sql_query(func):
    import sqlite3
    from contextlib import closing

    def wrapper(*args, **kwargs):
        with closing(sqlite3.connect('db/db.db')) as connect:
            try:
                connect.row_factory = sqlite3.Row
                cursor = connect.cursor()
                return func(*args, cursor, **kwargs)
            except sqlite3.DatabaseError:
                print(f"[-] Database ERROR while executing a function {str(func)}")
    return wrapper


@sql_query
def get_row(table, column, value, cursor):
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = {value}")
    return dict(cursor.fetchone())


@sql_query
def get_all(table, column, cursor, value=False):
    if value:
        cursor.execute(f"SELECT * FROM {table} WHERE {column} = {value}")
    else:
        cursor.execute(f"SELECT * FROM {table} WHERE {column} IS NULL")
    return [dict(row) for row in cursor.fetchall()]


@sql_query
def get_type_id(string, cursor):
    cursor.execute(f"SELECT typeID FROM invTypes WHERE typeName = '{string}'")
    result = cursor.fetchone()
    if result:
        return dict(result)['typeID']
    else:
        print(f"[-] {string} not found.")


@sql_query
def get_name(obj_id, cursor):
    if len(str(obj_id)) < 7:
        col, tab, name = 'typeID', 'invTypes', 'typeName'
    else:
        match str(obj_id)[0]:
            case '1':
                col, tab, name = 'regionID', 'mapRegions', 'regionName'
            case '2':
                col, tab, name = 'constellationID', 'mapConstellations', 'constellationName'
            case '3':
                col, tab, name = 'solarSystemID', 'mapSolarSystems', 'solarSystemName'
            case _:
                print(f"[-] {obj_id} not found!")
                return None
    cursor.execute(f"SELECT {name} FROM {tab} WHERE {col} = '{obj_id}'")
    result = list(cursor.fetchone())[0]
    return result


@sql_query
def get_npc_regions(cursor):
    cursor.execute(f"SELECT regionID FROM mapRegions WHERE factionID NOT NULL and factionID <> 500005")
    return [i[0] for i in cursor.fetchall()]

