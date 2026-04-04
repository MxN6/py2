import csv
from datetime import datetime
import psycopg2
from config import load_config

### TABLES ###

def create_table():

    """ Create tables in the PostgreSQL database"""
    commands = """
        CREATE TABLE contacts (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),
            phone_number VARCHAR(20) NOT NULL,
            type VARCHAR(20),
            email VARCHAR(40),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                cur.execute(commands)
    except (psycopg2.DatabaseError, Exception) as error:
        print("error:",error)

### INSERTS ###

def insert_contact(first_name, last_name, phone_num, typenum=None, email=None):
    """
    first_name: First name of the contact
    last_name: Last name of the contact
    """

    sql = """INSERT INTO contacts(first_name, last_name, phone_number, type, email)
             VALUES(%s, %s, %s, %s, %s) RETURNING id;"""

    id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, phone_num, typenum, email))
                row = cur.fetchone()
                if row:
                    id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("error:",error)
        return None

    return id

def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id = insert_contact(row['first_name'], row['last_name'], row['phone_number'], row.get('type'), row.get('email'))

### UPDATES ###

def update_contact_name(id, first_name, last_name=None):
    """ Update contact name based on the contact id """

    updated_row_count = 0

    sql = """ UPDATE contacts
                SET first_name = %s,
                last_name = COALESCE(%s, last_name)
                WHERE id = %s"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the UPDATE statement
                cur.execute(sql, (first_name, last_name, id))
                updated_row_count = cur.rowcount
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return updated_row_count

if __name__=='__main__':
    pass