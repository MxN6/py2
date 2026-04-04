CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts AS c
        WHERE c.first_name = p_first_name AND c.last_name = p_last_name
    ) THEN
        UPDATE contacts AS c
        SET c.phone_number = p_phone
        WHERE c.first_name = p_first_name AND c.last_name = p_last_name;
    ELSE
        INSERT INTO contacts(first_name, last_name, phone_number)
        VALUES (p_first_name, p_last_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    names TEXT[],
    phones TEXT[]
)
AS $$
DECLARE
    i INT;
    invalid_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(names, 1)
    LOOP
        IF phones[i] ~ '^\+[0-9]+$' AND length(phones[i]) >= 7 THEN
            INSERT INTO contacts(first_name, phone_number)
            VALUES (names[i], phones[i]);
        ELSE
            invalid_data := invalid_data || names[i] || ':' || phones[i] || '; ';
        END IF;
    END LOOP;

    RAISE NOTICE 'Invalid data: %', invalid_data;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR phone_number = p_value;
END;
$$ LANGUAGE plpgsql;