# /// script
# dependencies = [
#   "mysql-connector-python>=8.4.0",
#   "pydantic-settings>=1.0",
# ]
# ///
import json

import mysql.connector  # Ensure mysql-connector-python>=8.4.0 is installed
from pydantic_settings import BaseSettings

class Settings(BaseSettings, cli_parse_args=True):
    host: str = "localhost"
    user: str = "your_mysql_username"
    password: str = "your_mysql_password"
    database: str = "testdb"
    json_file: str = "https://peps.python.org/api/peps.json"

def main():
    settings = Settings()

    # First, connect without specifying a database to create it if necessary
    conn = mysql.connector.connect(
        host=settings.host,
        user=settings.user,
        password=settings.password,
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.database}")
    conn.commit()
    conn.close()

    # Now connect using the newly created database
    conn = mysql.connector.connect(
        host=settings.host,
        user=settings.user,
        password=settings.password,
        database=settings.database,
    )
    cursor = conn.cursor()

    import os
    if settings.json_file.startswith("http://") or settings.json_file.startswith("https://"):
        import urllib.request
        response = urllib.request.urlopen(settings.json_file)
        data = json.loads(response.read())
    else:
        with open(settings.json_file, "r") as f:
            data = json.load(f)
    # Derive table name from the supplied JSON file
    table = os.path.basename(settings.json_file)
    if table.lower().endswith(".json"):
        table = table[:-5]

    # Infer table schema automatically from the first record
    def infer_mysql_type(value):
        if isinstance(value, int):
            return "INT"
        elif isinstance(value, float):
            return "FLOAT"
        elif isinstance(value, bool):
            return "BOOLEAN"
        else:
            return "TEXT"

    # The JSON is assumed to be a dict where keys are pep IDs and values are detail dicts
    sample_key = next(iter(data))
    sample_record = data[sample_key]

    # Build dynamic CREATE TABLE statement for table derived from the JSON filename
    columns = []
    pk_col = f"{table}_id"
    columns.append(f"{pk_col} VARCHAR(255) PRIMARY KEY")
    for col, val in sample_record.items():
        columns.append(f"`{col}` {infer_mysql_type(val)}")
    create_table_sql = "CREATE TABLE IF NOT EXISTS " + table + " (" + ", ".join(columns) + ")"
    cursor.execute(create_table_sql)

    # Prepare bulk insert for all records using the dynamic table name and pk
    cols = [pk_col] + list(sample_record.keys())
    placeholders = ", ".join(["%s"] * len(cols))
    insert_sql = "INSERT INTO " + table + " (" + ", ".join(cols) + ") VALUES (" + placeholders + ")"

    # Helper function to transform list/dict values into JSON strings
    def transform_value(val):
        if isinstance(val, (list, dict)):
            return json.dumps(val)
        return val

    # Build row data using a list comprehension with value transformation
    rows = [
        [pep_id] + [transform_value(record.get(col)) for col in sample_record.keys()]
        for pep_id, record in data.items()
    ]
    cursor.executemany(insert_sql, rows)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
