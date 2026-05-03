import csv
import json
import os
from config import load_config
from connect import connect


# Создание таблиц

def create_tables(conn):
    """Create all tables if they don't exist."""
    cur = conn.cursor()

    # Основная таблица контактов 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id    SERIAL PRIMARY KEY,
            name  VARCHAR(255) NOT NULL,
            phone VARCHAR(20)  NOT NULL
        )
    """)

    # Таблица групп
    cur.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    """)

    # Стандартные группы
    cur.execute("""
        INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
        ON CONFLICT (name) DO NOTHING
    """)

    # Новые поля в contacts
    cur.execute("ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email    VARCHAR(100)")
    cur.execute("ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE")
    cur.execute("ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id)")
    cur.execute("ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()")

    # Таблица телефонов (несколько номеров у одного контакта)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id         SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
            phone      VARCHAR(20)  NOT NULL,
            type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
        )
    """)

    conn.commit()
    cur.close()


# Создание процедур и функций

def create_procedures(conn):
    """Create all stored procedures and functions."""
    cur = conn.cursor()

    # Удаляем старые версии чтобы не было конфликтов
    cur.execute("DROP FUNCTION IF EXISTS get_contacts_paginated(INTEGER, INTEGER)")
    cur.execute("DROP FUNCTION IF EXISTS search_contacts_by_pattern(VARCHAR)")
    cur.execute("DROP FUNCTION IF EXISTS search_contacts(TEXT)")
    cur.execute("DROP PROCEDURE IF EXISTS upsert_contact(VARCHAR, VARCHAR)")
    cur.execute("DROP PROCEDURE IF EXISTS insert_many_contacts(VARCHAR[], VARCHAR[])")
    cur.execute("DROP PROCEDURE IF EXISTS delete_contact(VARCHAR)")
    cur.execute("DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR)")
    cur.execute("DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR)")
    conn.commit()

    # Вставить или обновить контакт (Practice 8)
    cur.execute("""
        CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
        AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
                UPDATE contacts SET phone = p_phone WHERE name = p_name;
            ELSE
                INSERT INTO contacts(name, phone) VALUES (p_name, p_phone);
            END IF;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Массовая вставка с проверкой (Practice 8)
    cur.execute(r"""
        CREATE OR REPLACE PROCEDURE insert_many_contacts(names VARCHAR[], phones VARCHAR[])
        AS $$
        DECLARE i INTEGER;
        BEGIN
            FOR i IN 1..array_length(names, 1) LOOP
                IF phones[i] ~ '^[0-9+\-() ]{7,20}$' THEN
                    CALL upsert_contact(names[i], phones[i]);
                ELSE
                    RAISE NOTICE 'Skipped: % (phone=%)', names[i], phones[i];
                END IF;
            END LOOP;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Удаление по имени или телефону (Practice 8)
    cur.execute("""
        CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
        AS $$
        BEGIN
            DELETE FROM contacts WHERE name = p_value OR phone = p_value;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Поиск по имени или телефону (Practice 8)
    cur.execute("""
        CREATE OR REPLACE FUNCTION search_contacts_by_pattern(pattern VARCHAR)
        RETURNS TABLE (id INTEGER, name VARCHAR, phone VARCHAR)
        AS $$
        BEGIN
            RETURN QUERY
            SELECT c.id, c.name, c.phone
            FROM contacts c
            WHERE c.name ILIKE '%' || pattern || '%'
               OR c.phone ILIKE '%' || pattern || '%';
        END;
        $$ LANGUAGE plpgsql
    """)

    # Пагинация (Practice 8)
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INTEGER, p_offset INTEGER)
        RETURNS TABLE (id INTEGER, name VARCHAR, phone VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR)
        AS $$
        BEGIN
            RETURN QUERY
            SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            LIMIT p_limit OFFSET p_offset;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Добавить телефон к контакту (TSIS 1)
    cur.execute("""
        CREATE OR REPLACE PROCEDURE add_phone(
            p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR
        )
        AS $$
        DECLARE v_id INTEGER;
        BEGIN
            SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
            IF v_id IS NULL THEN
                RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
            END IF;
            INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
        END;
        $$ LANGUAGE plpgsql
    """)

    # Переместить контакт в группу (TSIS 1)
    cur.execute("""
        CREATE OR REPLACE PROCEDURE move_to_group(
            p_contact_name VARCHAR, p_group_name VARCHAR
        )
        AS $$
        DECLARE v_group_id INTEGER; v_contact_id INTEGER;
        BEGIN
            SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
            IF v_group_id IS NULL THEN
                INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
            END IF;
            SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
            IF v_contact_id IS NULL THEN
                RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
            END IF;
            UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Расширенный поиск по всем полям (TSIS 1)
    cur.execute("""
        CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
        RETURNS TABLE (
            contact_id INTEGER, contact_name VARCHAR, contact_phone VARCHAR,
            contact_email VARCHAR, contact_birthday DATE, group_name VARCHAR
        )
        AS $$
        BEGIN
            RETURN QUERY
            SELECT DISTINCT c.id, c.name, c.phone, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE c.name  ILIKE '%' || p_query || '%'
               OR c.phone ILIKE '%' || p_query || '%'
               OR c.email ILIKE '%' || p_query || '%'
               OR p.phone ILIKE '%' || p_query || '%';
        END;
        $$ LANGUAGE plpgsql
    """)

    conn.commit()
    cur.close()


# Вставка контактов

def insert_contact(conn, name, phone):
    """Insert or update a contact."""
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()


def insert_from_console(conn):
    """Add a contact from console input."""
    name = input("Name: ")
    phone = input("Phone: ")

    email = input("Email (Enter to skip): ").strip()
    birthday = input("Birthday YYYY-MM-DD (Enter to skip): ").strip()
    phone_type = input("Phone type - home/work/mobile (Enter to skip): ").strip().lower()
    group = input("Group - Family/Work/Friend/Other (Enter to skip): ").strip()

    try:
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

        if email:
            cur.execute("UPDATE contacts SET email = %s WHERE name = %s", (email, name))
        if birthday:
            cur.execute("UPDATE contacts SET birthday = %s WHERE name = %s", (birthday, name))
        if phone_type in ('home', 'work', 'mobile'):
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        if group:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))

        conn.commit()
        cur.close()

        print(f"Contact saved: {name}")
    except Exception as e:
        conn.rollback()
        print(f"Error saving contact: {e}")


def insert_from_csv(conn, filename):
    """Import from CSV. Supports new fields: email, birthday, group, phone_type."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        cur = conn.cursor()
        for row in reader:
            name = row['name']
            phone = row['phone']

            # Upsert основного контакта
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

            # Email
            if 'email' in headers and row.get('email'):
                cur.execute("UPDATE contacts SET email = %s WHERE name = %s", (row['email'], name))

            # День рождения
            if 'birthday' in headers and row.get('birthday'):
                cur.execute("UPDATE contacts SET birthday = %s WHERE name = %s", (row['birthday'], name))

            # Группа
            if 'group' in headers and row.get('group'):
                cur.execute("CALL move_to_group(%s, %s)", (name, row['group']))

            # Тип телефона -> phones
            if 'phone_type' in headers and row.get('phone_type'):
                ptype = row['phone_type'].lower()
                if ptype in ('home', 'work', 'mobile'):
                    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))

        conn.commit()
        cur.close()

    print(f"Imported from {filename}")


# Показ контактов

def get_all_contacts(conn, limit=50, offset=0):
    """Get contacts with pagination."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    return rows


def search_by_pattern(conn, pattern):
    """Search by name or phone (Practice 8)."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    cur.close()
    return rows


def print_contacts(contacts):
    """Simple output: id, name, phone."""
    if not contacts:
        print("  (no contacts)")
        return
    for c in contacts:
        print(f"  [{c[0]}] {c[1]} — {c[2]}")


def print_contacts_full(contacts, conn):
    """Full output: all fields + extra phones."""
    if not contacts:
        print("  (no contacts)")
        return
    for c in contacts:
        cid = c[0]
        name = c[1]
        phone = c[2]
        email = c[3] if c[3] else "—"
        birthday = str(c[4]) if c[4] else "—"
        group = c[5] if c[5] else "—"

        print(f"  [{cid}] {name}")
        print(f"       Phone:       {phone}")
        print(f"       Email:       {email}")
        print(f"       Birthday:    {birthday}")
        print(f"       Group:       {group}")

        # Доп. телефоны из таблицы phones
        cur = conn.cursor()
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
        extra = cur.fetchall()
        cur.close()
        for p in extra:
            print(f"       Phone ({p[1]}): {p[0]}")
        print()


# Обновление и удаление

def update_phone(conn, name, new_phone):
    """Update phone by name."""
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, new_phone))
    conn.commit()
    cur.close()
    print(f"Updated phone for {name}")


def update_name(conn, phone, new_name):
    """Update name by phone."""
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET name = %s WHERE phone = %s", (new_name, phone))
    conn.commit()
    print(f"Updated {cur.rowcount} row(s)")
    cur.close()


def delete_by_name(conn, name):
    """Delete contact by name."""
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (name,))
    conn.commit()
    cur.close()
    print(f"Deleted: {name}")


def delete_by_phone(conn, phone):
    """Delete contact by phone."""
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (phone,))
    conn.commit()
    cur.close()
    print(f"Deleted by phone: {phone}")


# Расширенный поиск и фильтрация (TSIS 1)

def extended_search(conn, query):
    """Search all fields: name, phone, email, all numbers."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    cur.close()
    return rows


def filter_by_group(conn, group_name):
    """Show contacts from a specific group."""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name
    """, (group_name,))
    rows = cur.fetchall()
    cur.close()
    return rows


def search_by_email(conn, email_part):
    """Search by email (partial match)."""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.name
    """, (f'%{email_part}%',))
    rows = cur.fetchall()
    cur.close()
    return rows


def sort_contacts(conn, sort_by):
    """Sort contacts by: name, birthday, or date."""
    order_map = {'name': 'c.name', 'birthday': 'c.birthday NULLS LAST', 'date': 'c.created_at'}
    order = order_map.get(sort_by, 'c.name')

    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order}
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


# Добавить телефон / Переместить в группу (TSIS 1)

def add_phone_to_contact(conn):
    """Add an extra phone number to a contact."""
    name = input("Contact name: ")
    phone = input("Phone number: ")
    ptype = input("Type (home/work/mobile): ").strip().lower()
    try:
        cur = conn.cursor()
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        cur.close()
        print(f"Added {ptype} phone {phone} to {name}")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")


def move_contact_to_group(conn):
    """Move a contact to a group."""
    name = input("Contact name: ")
    group = input("Group name: ")
    try:
        cur = conn.cursor()
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        cur.close()
        print(f"Moved {name} to group '{group}'")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")


# Пагинация с навигацией (TSIS 1)

def paginated_view(conn):
    """Paginated view: next / prev / quit."""
    page_size = 5
    offset = 0

    while True:
        page = (offset // page_size) + 1
        contacts = get_all_contacts(conn, page_size, offset)

        if not contacts and offset > 0:
            print("No more contacts.")
            offset -= page_size
            continue

        print(f"\n--- Page {page} ---")
        print_contacts_full(contacts, conn)

        choice = input("[n]ext / [p]rev / [q]uit: ").strip().lower()
        if choice == 'n':
            # Проверяем есть ли контакты на следующей странице
            next_page = get_all_contacts(conn, page_size, offset + page_size)
            if next_page:
                offset += page_size
            else:
                print("Last page.")
        elif choice == 'p':
            if offset > 0:
                offset -= page_size
            else:
                print("First page.")
        elif choice == 'q':
            break


# Экспорт и импорт JSON (TSIS 1)

def export_to_json(conn, filename):
    """Export all contacts to a JSON file."""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
    """)
    contacts = cur.fetchall()
    cur.close()

    result = []
    for c in contacts:
        cid, name, phone, email, birthday, group = c

        # Получаем доп. телефоны
        cur = conn.cursor()
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
        phones_list = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
        cur.close()

        result.append({
            "name": name,
            "phone": phone,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group,
            "phones": phones_list
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(result)} contacts to {filename}")


def import_from_json(conn, filename):
    """Import contacts from JSON. Asks skip or overwrite on duplicates."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        name = entry.get("name", "")
        phone = entry.get("phone", "")
        email = entry.get("email")
        birthday = entry.get("birthday")
        group = entry.get("group")
        phones = entry.get("phones", [])

        # Проверяем дубликат
        cur = conn.cursor()
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()
        cur.close()

        if existing:
            choice = input(f"'{name}' already exists. (s)kip or (o)verwrite? ").strip().lower()
            if choice != 'o':
                print(f"  Skipped: {name}")
                continue
            # Удаляем старые доп. телефоны
            cur = conn.cursor()
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing[0],))
            conn.commit()
            cur.close()

        # Upsert контакта
        insert_contact(conn, name, phone)

        # Email
        if email:
            cur = conn.cursor()
            cur.execute("UPDATE contacts SET email = %s WHERE name = %s", (email, name))
            conn.commit()
            cur.close()

        # День рождения
        if birthday:
            cur = conn.cursor()
            cur.execute("UPDATE contacts SET birthday = %s WHERE name = %s", (birthday, name))
            conn.commit()
            cur.close()

        # Группа
        if group:
            cur = conn.cursor()
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
            conn.commit()
            cur.close()

        # Доп. телефоны
        for p in phones:
            if p.get("phone") and p.get("type") in ('home', 'work', 'mobile'):
                cur = conn.cursor()
                cur.execute("CALL add_phone(%s, %s, %s)", (name, p["phone"], p["type"]))
                conn.commit()
                cur.close()

        print(f"  Imported: {name}")

    print("JSON import complete.")


# Главное меню

def main():
    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    create_tables(conn)
    create_procedures(conn)
    print("Ready!\n")

    while True:
        print("\n     PHONEBOOK (TSIS 1)")
        print()
        print("  1.  Show contacts (paginated)")
        print("  2.  Add contact")
        print("  3.  Import from CSV")
        print("  4.  Search (name/phone)")
        print("  5.  Update phone by name")
        print("  6.  Update name by phone")
        print("  7.  Delete by name")
        print("  8.  Delete by phone")
        print("  9.  Extended search (all fields)")
        print("  10. Filter by group")
        print("  11. Search by email")
        print("  12. Sort contacts")
        print("  13. Add phone to contact")
        print("  14. Move to group")
        print("  15. Export to JSON")
        print("  16. Import from JSON")
        print()
        print("  0.  Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            paginated_view(conn)

        elif choice == "2":
            insert_from_console(conn)

        elif choice == "3":
            f = input("CSV file (Enter = contacts.csv): ").strip()
            if not f:
                f = "contacts.csv"
            insert_from_csv(conn, f)

        elif choice == "4":
            p = input("Search: ")
            print_contacts(search_by_pattern(conn, p))

        elif choice == "5":
            name = input("Name: ")
            phone = input("New phone: ")
            update_phone(conn, name, phone)

        elif choice == "6":
            phone = input("Phone: ")
            name = input("New name: ")
            update_name(conn, phone, name)

        elif choice == "7":
            name = input("Name: ")
            delete_by_name(conn, name)

        elif choice == "8":
            phone = input("Phone: ")
            delete_by_phone(conn, phone)

        elif choice == "9":
            q = input("Search query: ")
            results = extended_search(conn, q)
            print_contacts_full(results, conn)

        elif choice == "10":
            cur = conn.cursor()
            cur.execute("SELECT name FROM groups ORDER BY name")
            groups = [g[0] for g in cur.fetchall()]
            cur.close()
            print("Groups:", ", ".join(groups))
            g = input("Filter by group: ")
            results = filter_by_group(conn, g)
            print_contacts_full(results, conn)

        elif choice == "11":
            e = input("Search email: ")
            results = search_by_email(conn, e)
            print_contacts_full(results, conn)

        elif choice == "12":
            print("Sort by: name / birthday / date")
            s = input("Sort by: ").strip().lower()
            if s not in ('name', 'birthday', 'date'):
                s = 'name'
            results = sort_contacts(conn, s)
            print_contacts_full(results, conn)

        elif choice == "13":
            add_phone_to_contact(conn)

        elif choice == "14":
            move_contact_to_group(conn)

        elif choice == "15":
            f = input("JSON file (Enter = contacts_export.json): ").strip()
            if not f:
                f = "contacts_export.json"
            export_to_json(conn, f)

        elif choice == "16":
            f = input("JSON file (Enter = contacts_export.json): ").strip()
            if not f:
                f = "contacts_export.json"
            import_from_json(conn, f)

        elif choice == "0":
            break

        else:
            print("Invalid choice")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()
