import psycopg2
from psycopg2.extras import DictCursor
from config import load_config

# region table
table_cmds = ("""
    CREATE TABLE IF NOT EXISTS groups (
        g_id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            email VARCHAR(100),
            birthday DATE,
            group_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups (g_id) ON UPDATE CASCADE ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS phones (
        p_id SERIAL PRIMARY KEY,
        phone VARCHAR(255) UNIQUE NOT NULL,
        type VARCHAR(255) CHECK (type IN ('home', 'work', 'mobile')),
        contact_id INT NOT NULL,
        FOREIGN KEY (contact_id) REFERENCES contacts (id) ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
)
# endregion

# region queries
iq_groups = """
    INSERT INTO groups ("name") 
    VALUES (%s)
"""
iq_contacts = """
    INSERT INTO contacts ("first_name", "last_name", "email", "birthday", "group_id") 
    VALUES (%s, %s, %s, %s, %s) 
"""
iq_phones = """
    INSERT INTO phones ("phone", "type", "contact_id") 
    VALUES (%s, %s, %s) 
"""
uq_contacts = """
    UPDATE contacts 
    SET "first_name" = %s, "last_name" = %s, "email" = %s, "birthday" = %s, "group_id" = %s 
    WHERE id = %s
"""
uq_phones = 'UPDATE phones SET "phone" = %s, "type" = %s, "contact_id" = %s WHERE p_id = %s'
sq_contacts_a = 'SELECT * FROM contacts'
sq_contacts_c = 'SELECT "first_name", "last_name", "email", "birthday", "group_id" FROM contacts WHERE id = %s'
#endregion

# region functions

def create_tables():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in table_cmds:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def insert_group(group : str):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(iq_groups, (group,))
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

def insert_contact(data : tuple):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(iq_contacts, data)
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

def insert_contacts(data: list):
    ids = []
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for row in data:
                    cur.execute(iq_contacts, row)
            conn.commit()
            return ids
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
        return None

def insert_phone(data : tuple):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(iq_phones, data)
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

def insert_phones(data : list):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(iq_phones, data)
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def update_contact(data : tuple):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(uq_contacts, data)
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

def update_phone(data : tuple):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(uq_phones, data)
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def select_all_contacts():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sq_contacts_a)
                return cur.fetchall()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

def select_contact(id : int):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sq_contacts_c, (id,))
                return cur.fetchone()
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

def select_contacts_dict():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(sq_contacts_a)
                # Fetch all rows as a list of dictionaries
                rows = [dict(row) for row in cur.fetchall()]
                return rows
    except(psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")

# endregion