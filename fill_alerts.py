# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, Error

# import Python's built-in JSON library
import json

# import the JSON library from psycopg2.extras
from psycopg2.extras import Json

# import psycopg2's 'json' using an alias
from psycopg2.extras import json as psycop_json

# import Python's 'sys' library
import sys


table_name = "alerts"

print("\ntable name for JSON data:", table_name)

# open alerts, store as json data
with open('alerts.json') as json_data:

    record_list = json.load(json_data)

print("\nrecords:", record_list)
# should return "<class 'list'>"
print("\nJSON records object type:", type(record_list))

# concatenate to a SQL string
sql_string = 'INSERT INTO {} '.format(table_name)

# if record_list is a list, then get column names from first key
if type(record_list) == list:
    first_record = record_list[0]

    columns = list(first_record.keys())
    print("\ncolumn names:", columns)

# if not, exit out
else:
    print("Needs to be an array of JSON objects")
    sys.exit()

# add () around sql_string to be a valid SQL statement
sql_string += "(" + ', '.join(columns) + ")\nVALUES "

# enumerate over the record
for i, record_dict in enumerate(record_list):

    # iterate over the values of each record dict object
    values = []
    for col_names, val in record_dict.items():

        # Postgres strings must be enclosed with single quotes
        if type(val) == str:
            # escape apostrophies with two single quotations
            val = val.replace("'", "''")
            val = "'" + val + "'"

        values += [str(val)]

    # join the list of values and enclose record in parenthesis
    sql_string += "(" + ', '.join(values) + "),\n"

# remove the last comma and end statement with a semicolon
sql_string = sql_string[:-2] + ";"


try:
    conn = connect(
        dbname="rocketdb",
        user="postgres",
        host="localhost",  # !UPDATE TO HEROKU ADDRESS WHEN APPLICABLE,
        password="number13",  # !ENV VAR THIS
        connect_timeout=3
    )
    cur = conn.cursor()
    print("\ncreated cursor obj:", cur)
except (Exception, Error) as err:
    print("\npsycopg2 connect error:", err)
    conn = None
    cur = None

# * Attempt to execute SQL if cur is valid
if cur != None:
    try:
        cur.execute(sql_string)
        conn.commit()

        print('\nfinished INSERT INTO execution')
    except (Exception, Error) as err:
        print("\nexecute_sql() error:", err)
        conn.rollback()
    # close cur and conn
    cur.close()
    conn.close()

# print(sql_string)
