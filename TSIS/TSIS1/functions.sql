CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone_numbers TEXT,  -- Aggregated list of phones
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
    ORDER BY c.first_name ASC -- Sorting by name makes navigation intuitive
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;