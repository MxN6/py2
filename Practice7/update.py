import psycopg2
from config import load_config


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

if __name__ == '__main__':
    update_contact_name(1, "Tomatoma")

