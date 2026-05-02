import csv
import psycopg2
from psycopg2.extras import DictCursor
from config import load_config

DEFAULT_GROUPS = ["Family", "Work", "Friend", "Other"]

TABLE_COMMANDS = (
    """
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
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
        FOREIGN KEY (group_id) REFERENCES groups (id) ON UPDATE CASCADE ON DELETE SET NULL
    )
    """,
    """
    ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100)
    """,
    """
    ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE
    """,
    """
    ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id)
    """,
    """
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        phone VARCHAR(255) UNIQUE NOT NULL,
        type VARCHAR(255) CHECK (type IN ('home', 'work', 'mobile')),
        contact_id INT NOT NULL,
        FOREIGN KEY (contact_id) REFERENCES contacts (id) ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
)

IQ_GROUPS = """
    INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING
"""
IQ_CONTACTS = """
    INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
"""
IQ_PHONES = """
    INSERT INTO phones (phone, type, contact_id)
    VALUES (%s, %s, %s)
    ON CONFLICT (phone) DO NOTHING
"""
UQ_CONTACTS = """
    UPDATE contacts
    SET first_name = %s,
        last_name = %s,
        email = %s,
        birthday = %s,
        group_id = %s
    WHERE id = %s
"""
SQ_CONTACTS_ALL = 'SELECT * FROM contacts'
SQ_CONTACT_WITH_ID = 'SELECT first_name, last_name, email, birthday, group_id FROM contacts WHERE id = %s'


def _connect():
    return psycopg2.connect(**load_config())


def initialize_database():
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                for command in TABLE_COMMANDS:
                    cur.execute(command)
            conn.commit()
        for group in DEFAULT_GROUPS:
            insert_group(group)
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Database error: {error}")


def insert_group(group: str):
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(IQ_GROUPS, (group,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def get_group_id(group_name: str, create: bool = True):
    if not group_name:
        return None
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM groups WHERE name = %s', (group_name,))
                row = cur.fetchone()
                if row:
                    return row[0]
                if create:
                    cur.execute('INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING', (group_name,))
                    conn.commit()
                    cur.execute('SELECT id FROM groups WHERE name = %s', (group_name,))
                    row = cur.fetchone()
                    return row[0] if row else None
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return None


def find_contact(first_name: str, last_name: str):
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id FROM contacts WHERE first_name = %s AND last_name = %s',
                    (first_name, last_name),
                )
                row = cur.fetchone()
                return row[0] if row else None
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return None


def insert_contact(data: dict):
    try:
        group_id = get_group_id(data.get('group'))
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    IQ_CONTACTS,
                    (
                        data.get('first_name'),
                        data.get('last_name'),
                        data.get('email'),
                        data.get('birthday'),
                        group_id,
                    ),
                )
                contact_id = cur.fetchone()[0]
            conn.commit()
        return contact_id
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return None


def insert_phones(contact_id: int, phones: list):
    try:
        if not phones:
            return
        args = [(phone['phone'], phone['type'], contact_id) for phone in phones]
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.executemany(IQ_PHONES, args)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def delete_phones(contact_id: int):
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM phones WHERE contact_id = %s', (contact_id,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def update_contact(contact_id: int, data: dict):
    try:
        group_id = get_group_id(data.get('group'))
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    UQ_CONTACTS,
                    (
                        data.get('first_name'),
                        data.get('last_name'),
                        data.get('email'),
                        data.get('birthday'),
                        group_id,
                        contact_id,
                    ),
                )
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def select_groups():
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT name FROM groups ORDER BY name')
                return [row[0] for row in cur.fetchall()]
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return []


def select_contacts_with_filters(group_name=None, email_query=None, order_by='name', limit=10, offset=0):
    order_options = {
        'name': 'c.first_name, c.last_name',
        'birthday': 'c.birthday NULLS LAST',
        'date': 'c.created_at DESC',
    }
    order_clause = order_options.get(order_by, order_options['name'])
    query = """
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.birthday,
            c.created_at,
            g.name as group_name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
    """
    conditions = []
    params = []
    if group_name:
        conditions.append('g.name = %s')
        params.append(group_name)
    if email_query:
        conditions.append('c.email ILIKE %s')
        params.append(f'%{email_query}%')
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    query += f' ORDER BY {order_clause} LIMIT %s OFFSET %s'
    params.extend([limit, offset])

    try:
        with _connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, tuple(params))
                rows = [dict(row) for row in cur.fetchall()]
                contacts = {}
                for row in rows:
                    contact_id = row['id']
                    if contact_id not in contacts:
                        contacts[contact_id] = {
                            'id': contact_id,
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'email': row['email'],
                            'birthday': row['birthday'],
                            'created_at': row['created_at'],
                            'group': row['group_name'] or 'Other',
                            'phones': [],
                        }
                    if row['phone']:
                        contacts[contact_id]['phones'].append({'phone': row['phone'], 'type': row['type']})
                return list(contacts.values())
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return []


def select_contacts_paginated(limit_val: int, offset_val: int):
    try:
        with _connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM get_contacts_paginated(%s, %s)', (limit_val, offset_val))
                return [dict(row) for row in cur.fetchall()]
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return []


def search_contacts(query: str):
    try:
        with _connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM search_contacts(%s)', (query,))
                return [dict(row) for row in cur.fetchall()]
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")
    return []


def add_phone_procedure(contact_name: str, phone: str, phone_type: str):
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute('CALL add_phone(%s, %s, %s)', (contact_name, phone, phone_type))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def move_to_group_procedure(contact_name: str, group_name: str):
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute('CALL move_to_group(%s, %s)', (contact_name, group_name))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"PostgreSQL error: {error}")


def select_contacts_dict():
    return select_contacts_with_filters(limit=1000, offset=0)
