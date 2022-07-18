from re import I, M
import sqlite3
import json
from models import Journalentries, Mood, entrytag, Tags


def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id, 
            m.label mood_label 
        FROM Journalentries a
        JOIN Moods m
            ON m.id = a.mood_id
        
        """)

        journalentries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            entry = Journalentries(row['id'], row['date'], row['concept'], row['entry'],
                                row['mood_id'])
            mood = Mood(row['mood_id'], row['mood_label'])
            entry.mood = mood.__dict__
            #Make sql call to get the tag ids / names for this entry.
            db_cursor.execute("""
            SELECT
                e.tag_id,
                t.name
            FROM entrytags e
            JOIN Tags t
                ON e.tag_id = t.id
            WHERE e.entry_id = ?
            """, (row['id'], ))
            # make a spot for the tags
            tagsList = []
            #Store response from SQL call to tagData
            tagData = db_cursor.fetchall()

            #Loop through rows from SQL call 
            for row in tagData:

                #make a tag instance with stuff in each row
                tag = Tags(row['tag_id'], row['name'])

                #turn this instance into a dictionary, append dictionary to tags list
                tagsList.append(tag.__dict__)

            #Add tags list to entry
            entry.tags = tagsList

            journalentries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(journalentries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id
        FROM Journalentries a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Journalentries(data['id'], data['date'], data['concept'], data['entry'], data['mood_id'])
    return json.dumps(entry.__dict__)

def get_search_entry(search_terms):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT *
	    FROM Journalentries 
        WHERE entry LIKE ?

        """, (f"%{search_terms}%", ))
        journalList = []

        # Load the single result into memory
        dataset = db_cursor.fetchall()
        for row in dataset:

        # Create an animal instance from the current row
            entry = Journalentries(row['id'], row['date'], row['concept'], row['entry'], row['mood_id'])
            journalList.append(entry.__dict__)

        return json.dumps(journalList)

def create_new_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Journalentries
            ( date, concept, entry, mood_id )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['date'], new_entry['concept'], new_entry['entry'], new_entry['moodId']))
        id = db_cursor.lastrowid
        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id
        #loop through tags execute sql to add a row to the etnrytagsdatabase
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entryTags
                ( entry_Id, tag_id )
            VALUES
                ( ?, ?);
            """, (id, tag,))



    return json.dumps(new_entry)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM journalentries
        WHERE id = ?
        """, (id, ))

def update_entry(id, updated_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Journalentries
            SET
                date = ?,
                concept = ?,
                entry = ?,
                mood_id = ?
        WHERE id = ?
        """, (updated_entry['date'], updated_entry['concept'], updated_entry['entry'], updated_entry['moodId'],  id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

