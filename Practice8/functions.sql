CREATE OR REPLACE FUNCTION search_contacts_by_pattern(pattern VARCHAR)
RETURNS TABLE (id INTEGER, name VARCHAR(255), phone VARCHAR(20))
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || pattern || '%'
       OR c.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(page_limit INTEGER, page_offset INTEGER)
RETURNS TABLE (id INTEGER, name VARCHAR(255), phone VARCHAR(20))
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT page_limit OFFSET page_offset;
END;
$$ LANGUAGE plpgsql;