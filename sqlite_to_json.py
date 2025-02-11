import sqlite3
import json
import os

def sqlite_to_json(db_file, output_dir):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for table_name in tables:
        table_name = table_name[0]

        # Fetch all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert rows to a list of dictionaries
        table_data = [dict(zip(column_names, row)) for row in rows]

        # Write the table data to a JSON file
        output_file = os.path.join(output_dir, f"{table_name}.json")
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(table_data, json_file, indent=4)

        print(f"Exported table '{table_name}' to {output_file}")

    # Close the connection
    conn.close()

# Example usage
sqlite_db_file = "mock_cfo.db"  # Replace with your SQLite file
output_directory = "output_json"    # Replace with your desired output directory
sqlite_to_json(sqlite_db_file, output_directory)
