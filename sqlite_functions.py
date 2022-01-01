import sqlite3
from sqlite3 import Error
import os
import datetime


def main():

    # main program

    table = "posts"
    database = f"{os.getcwd()}/fastapi_sm.db"

    # create db (for first instance only) - if exist then close

    create_db(database)

    with create_connection(database) as conn:

        # create table (for first instance of needed table only)

        create_table(
            conn,
            f"""
            -- https://sqlite.org/datatype3.html

            create table if not exists {table} (

                id integer PRIMARY KEY,

                title varchar NOT NULL,
                content varchar NOT NULL,
                published boolean DEFAULT false,
                created_at timestamp DEFAULT (datetime('now','+8 hours'))
            );
            """
        )

        delete_table(conn, "users_testing")

        # -- amendments to table: insert/update data point ---------------------

        data = {
            "title": "second post",
            "content": "yada yada",
            "published": True
        }

        # insert data point
        # insert_data(conn, data, table)

        # update data point
        # update_data(conn, data, 1, table)

        # delete data point
        # delete_data(conn, 1, table)

        # delete all data points
        # delete_all_data(conn, table)

        # -- query data --------------------------------------------------------

        query_sql = f"""
        -- https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

        select *
        from {table};
        """

        result = query(conn, query_sql)


# -- sqlite functions ----------------------------------------------------------

def create_db(database):
    """ Create Database

    https://www.sqlitetutorial.net/sqlite-python/creating-database/

    create db file

    :param database: db file name and directory
    :return:
    """

    try:
        conn = sqlite3.connect(database)
        print(f"[Connected] sqlite3 --ver: {sqlite3.version}\n")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(database):
    """ Create Connection

    create db connection to the SQLite db based on file

    :param database: db file (by directory)
    :return: Connection object or None
    """

    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """ Create Table

    create a table from create_table_sql statement

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: null
    """

    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)


def delete_table(conn, table_name):
    """ Create Table

    create a table from create_table_sql statement

    :param conn: Connection object
    :param table_name: a DROP TABLE {name} statement
    :return: null
    """

    cursor = conn.cursor()
    cursor.execute(f"drop table {table_name}")
    conn.commit()


def insert_data(conn, data, table):
    """ Insert Data

    insert a new data point into the table

    :param conn: connection to db
    :param data: input values to be inserted into table
    :return: print id of last row
    """

    cursor = conn.cursor()

    data_items = list(filter(lambda x: x[1] is not None, data.items()))
    cols = tuple(key for key, val in data_items)
    vals = tuple(val for key, val in data_items)

    insert_sql = f"""
    insert into {table} ({",".join(cols)})
    values ({",".join("?" * len(cols))})
    """

    print(insert_sql)

    cursor.execute(insert_sql, vals)

    # commit changes w/o close
    conn.commit()

    print(f"id gen: {cursor.lastrowid}\n")

    return cursor.lastrowid


def update_data(conn, data, id, table):
    """ update existing data point in table

    :param conn: connection to db
    :param data: input values to be updated based on id
    :param id: selected id to be updated with data values
    :return:
    """

    # NOTE: change logic for data dictionary
    cursor = conn.cursor()

    data_items = list(filter(lambda x: x[1] is not None, data.items()))
    cols = ",".join([f"{key}=?" for key, val in data_items])
    vals = tuple(val for key, val in data_items)

    update_query = f"""
        update {table}
        set {cols}
        where id = ?
        """

    cursor.execute(update_query, (*vals, id))

    # commit changes w/o close
    conn.commit()


def delete_data(conn, id, table):
    """ Delete Data

    delete existing data point in table

    :param conn: connection to db
    :param id: selected id to be deleted from table
    :return:
    """

    cursor = conn.cursor()

    cursor.execute(
        f"""
        delete from {table}
        where id = ?;
        """,
        (id,)
    )

    # commit changes w/o close
    conn.commit()


def delete_all_data(conn, table):
    """ Delete All Data

    delete all data point in table

    :param conn: connection to db
    :return:
    """

    cursor = conn.cursor()

    cursor.execute(
        f"""
        delete from {table};
        """,
        ()
    )

    # commit changes w/o close
    conn.commit()


def query(conn, query_sql):
    """ Query Data

    Query all rows in the table

    :param conn: connection to db
    :return:
    """

    # https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

    cursor = conn.cursor()

    # query

    cursor.execute(query_sql)

    # return records (options: fetchone, fetchmany)

    records = cursor.fetchall()

    headers = list(map(lambda x: x[0], cursor.description))

    print_special("query output below")

    print(*headers)
    for row in records:
        print(*row)

    return records


def print_special(text, max_char=80, start_chars=5, gaps_chars=2):

    remainder = max_char - len(text) - start_chars - gaps_chars
    text_start, text_end = "=" * start_chars, "=" * remainder

    print(f"{text_start} {text.upper()} {text_end}\n")


# execution: python program file
if __name__ == "__main__":
    main()
