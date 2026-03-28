import psycopg2
from config import load_config
def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE contacts (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """ 
        CREATE TABLE phone_numbers (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            contact_id INTEGER,
            phone_number VARCHAR(20) NOT NULL,
            type VARCHAR(20),
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE emails (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            contact_id INTEGER,
            email VARCHAR(40),
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
if __name__ == '__main__':
    create_tables()