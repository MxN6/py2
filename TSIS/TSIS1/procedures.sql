CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR,
    p_email VARCHAR DEFAULT NULL
)
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts 
    WHERE first_name = p_first_name AND last_name = p_last_name;

    IF v_contact_id IS NOT NULL THEN
        UPDATE contacts SET email = p_email WHERE id = v_contact_id;
        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, 'mobile')
        ON CONFLICT (phone) DO NOTHING;
    ELSE
        INSERT INTO contacts(first_name, last_name, email)
        VALUES (p_first_name, p_last_name, p_email)
        RETURNING id INTO v_contact_id;

        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_contact_id, p_phone, 'mobile');
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value 
       OR id IN (SELECT contact_id FROM phones WHERE phone = p_value);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE first_name = p_contact_name;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_id, p_phone, p_type)
        ON CONFLICT (phone) DO NOTHING;
    ELSE
        RAISE NOTICE 'Contact % not found.', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone_numbers TEXT,
    group_name VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phone_numbers,
        g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name  ILIKE '%' || p_query || '%'
       OR c.email      ILIKE '%' || p_query || '%'
       OR p.phone      ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_val INT, offset_val INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, 
        c.first_name, 
        c.last_name, 
        c.email, 
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.first_name ASC, c.last_name ASC
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;
