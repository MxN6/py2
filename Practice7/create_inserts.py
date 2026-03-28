import csv
import psycopg2
from config import load_config
from datetime import datetime

def insert_contact(first_name, last_name=None, created_at=None):
    """ Insert a new contact into the contacts table """
    if created_at is None:
        created_at = datetime.now()  # use default timestamp

    sql = """INSERT INTO contacts(first_name, last_name, created_at)
             VALUES(%s, %s, %s) RETURNING id;"""

    id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, created_at))
                row = cur.fetchone()
                if row:
                    id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

    return id

def insert_many_contacts(contact_list):
    """ Insert multiple contacts into the contacts table  """
    sql = """INSERT INTO contacts(first_name, last_name)
             VALUES(%s, %s)"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, contact_list)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_email(contact_id, email):
    sql = """INSERT INTO emails(contact_id, email)
    VALUES (%s, %s) RETURNING id;"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (contact_id, email))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_phonenumber(contact_id, phone_number, type = 'Personal'):
    sql = """INSERT INTO phone_numbers(contact_id, phone_number, type)
    VALUES (%s, %s, %s) RETURNING id;"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (contact_id, phone_number, type))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id = insert_contact(row['first_name'], row.get('last_name'))
            insert_phonenumber(id, row['phone_number'])


if __name__ == '__main__':
    #insert_contact("Andrey", "Max")
    #insert_phonenumber(7, "+000000000", "Work")
    pass
    # insert_email(1, "Homelandre@gmail.com")
    # insert_phonenumber(1, "+777277727272", "Personal")
    
    # # single insert
    # insert_contact("Ashley", "Lukeatmi")

    # # multiple insert
    # insert_many_contacts([
    #     ("Bally", "Ler"),
    #     ("Kolly", "Kaw"),
    #     ("Dolly", "Ters"),
    #     ("Snap", "Shotte"),
    #     ("Neigher", "Runne")
    # ])