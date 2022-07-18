from models import Tags
import sqlite3
import json

def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name
        FROM Tags a
        """)

        tagsList = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            tag = Tags(row['id'], row['name'] )

    # Add the dictionary representation of the animal to the list
            tagsList.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tagsList)
