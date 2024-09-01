import sqlite3


# # get tables in the database
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()

# print("Tables in the database:")
# for table in tables:
#     print(table[0])


# get schema of a table
def table_infos(tables=[]):
    print("tables", tables)
    conn = sqlite3.connect("./data/Chinook.db")
    cursor = conn.cursor()
    table_data = []

    # loop through each table
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        schema = cursor.fetchall()

        table_schema = f"CREATE TABLE {table}:"
        for column in schema:
            # table_schema += f"\n    {column[1]} {column[2]} {column[3]},"
            table_schema += "\n    " + " ".join(map(str, column))

        table_data.append(table_schema)

    # close database
    conn.close()
    return "\n\n".join(table_data)


# execute a query
def query_data(sql_query):
    conn = sqlite3.connect("./data/Chinook.db")
    cursor = conn.cursor()

    # run the query
    cursor.execute(sql_query)
    data = cursor.fetchall()

    # close database
    conn.close()
    return data
