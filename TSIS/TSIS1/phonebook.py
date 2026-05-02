import csv
import json
import os
import datetime
import connect

DEFAULT_CSV = 'contacts.csv'
DEFAULT_IMPORT_JSON = 'contacts_import.json'
DEFAULT_EXPORT_JSON = 'contacts_export.json'
PAGE_SIZE = 4

VALID_PHONE_TYPES = {'home', 'work', 'mobile'}


def clean_text(value):
    return value.strip() if isinstance(value, str) else ''


def parse_date(value):
    value = clean_text(value)
    if not value:
        return None
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y'):
        try:
            return datetime.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    print(f"Warning: unsupported birthday format '{value}'. Use YYYY-MM-DD or DD.MM.YYYY.")
    return None


def normalize_group(group_value):
    value = clean_text(group_value)
    if not value:
        return 'Other'
    return value.title()


def normalize_phone_type(phone_type):
    value = clean_text(phone_type).lower()
    return value if value in VALID_PHONE_TYPES else 'mobile'


def format_contact(contact):
    lines = []
    full_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip()
    email = contact.get('email') or '-'
    birthday = contact.get('birthday') or '-'
    group = contact.get('group') or 'Other'
    lines.append(f"[{contact.get('id')}] {full_name} | {group} | {email} | {birthday}")
    for phone in contact.get('phones', []):
        lines.append(f"    - {phone.get('type', 'mobile').title()}: {phone.get('phone')}")
    return '\n'.join(lines)


def press_enter_to_continue():
    input('\nPress Enter to continue...')


def choose_sort_order():
    options = {'1': 'name', '2': 'birthday', '3': 'date'}
    print('Sort by:')
    print('  1) Name')
    print('  2) Birthday')
    print('  3) Date added')
    choice = input('Choose sort order [1-3]: ').strip()
    return options.get(choice, 'name')


def choose_group_filter():
    groups = connect.select_groups()
    if not groups:
        groups = ['Family', 'Work', 'Friend', 'Other']
    print('Group filter:')
    print('  0) All groups')
    for index, group in enumerate(groups, start=1):
        print(f'  {index}) {group}')
    choice = input('Choose a group [0-%s]: ' % len(groups)).strip()
    if choice == '0' or not choice:
        return None
    try:
        index = int(choice) - 1
        return groups[index] if 0 <= index < len(groups) else None
    except ValueError:
        return None


def load_csv_contacts(csv_path):
    if not os.path.exists(csv_path):
        print(f'CSV file not found: {csv_path}')
        return []

    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        contacts = {}
        for row in reader:
            first = clean_text(row.get('first_name'))
            last = clean_text(row.get('last_name'))
            if not first:
                continue
            email = clean_text(row.get('email'))
            birthday = row.get('birthday')
            birthday = parse_date(birthday)
            group_name = normalize_group(row.get('group') or row.get('group_name') or row.get('group_id'))
            phone = clean_text(row.get('phone'))
            phone_type = normalize_phone_type(row.get('type') or row.get('phone_type'))
            key = (first, last, email, birthday, group_name)
            if key not in contacts:
                contacts[key] = {
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                    'birthday': birthday,
                    'group': group_name,
                    'phones': [],
                }
            if phone:
                contacts[key]['phones'].append({'phone': phone, 'type': phone_type})
        return list(contacts.values())


def load_json_contacts(json_path):
    if not os.path.exists(json_path):
        print(f'JSON file not found: {json_path}')
        return []
    with open(json_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        contacts = []
        for item in data:
            first = clean_text(item.get('first_name'))
            last = clean_text(item.get('last_name'))
            if not first:
                continue
            email = clean_text(item.get('email'))
            birthday = parse_date(item.get('birthday'))
            group_name = normalize_group(item.get('group') or item.get('group_name') or item.get('group_id'))
            phones = []
            if isinstance(item.get('phones'), list):
                for phone_item in item['phones']:
                    phone_value = clean_text(phone_item.get('phone') if isinstance(phone_item, dict) else phone_item)
                    phone_type = normalize_phone_type(phone_item.get('type') if isinstance(phone_item, dict) else None)
                    if phone_value:
                        phones.append({'phone': phone_value, 'type': phone_type})
            elif item.get('phone'):
                phones.append({'phone': clean_text(item.get('phone')), 'type': normalize_phone_type(item.get('type'))})
            contacts.append({
                'first_name': first,
                'last_name': last,
                'email': email,
                'birthday': birthday,
                'group': group_name,
                'phones': phones,
            })
        return contacts


def export_contacts_to_json(json_path):
    contacts = connect.select_contacts_dict()
    if not contacts:
        print('No contacts available to export.')
        return
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(contacts, json_file, default=str, indent=2)
    print(f'Exported {len(contacts)} contacts to {json_path}')


def import_contacts_from_csv(csv_path):
    contacts = load_csv_contacts(csv_path)
    if not contacts:
        print('No rows were loaded from CSV.')
        return
    inserted = 0
    updated = 0
    for contact in contacts:
        existing_id = connect.find_contact(contact['first_name'], contact['last_name'])
        if existing_id:
            print(f"Contact already exists: {contact['first_name']} {contact['last_name']} (adding new phones)")
            connect.insert_phones(existing_id, contact['phones'])
            updated += 1
        else:
            contact_id = connect.insert_contact(contact)
            if contact_id:
                connect.insert_phones(contact_id, contact['phones'])
                inserted += 1
    print(f'CSV import completed: {inserted} added, {updated} updated.')


def import_contacts_from_json(json_path):
    contacts = load_json_contacts(json_path)
    if not contacts:
        print('No contacts loaded from JSON.')
        return
    inserted = 0
    skipped = 0
    overwritten = 0
    for contact in contacts:
        existing_id = connect.find_contact(contact['first_name'], contact['last_name'])
        if existing_id:
            answer = input(f"Duplicate found for {contact['first_name']} {contact['last_name']}. Skip or overwrite? [s/o]: ").strip().lower()
            if answer.startswith('o'):
                connect.update_contact(existing_id, contact)
                connect.delete_phones(existing_id)
                connect.insert_phones(existing_id, contact['phones'])
                overwritten += 1
            else:
                skipped += 1
        else:
            contact_id = connect.insert_contact(contact)
            if contact_id:
                connect.insert_phones(contact_id, contact['phones'])
                inserted += 1
    print(f'JSON import completed: {inserted} new, {overwritten} overwritten, {skipped} skipped.')


def display_contacts(contacts):
    if not contacts:
        print('No contacts found.')
        return
    for contact in contacts:
        print(format_contact(contact))
        print('-' * 80)


def browse_contacts():
    group_filter = choose_group_filter()
    sort_order = choose_sort_order()
    page = 0
    while True:
        offset = page * PAGE_SIZE
        contacts = connect.select_contacts_with_filters(
            group_name=group_filter,
            order_by=sort_order,
            limit=PAGE_SIZE,
            offset=offset,
        )
        if not contacts and page == 0:
            print('No contacts found for that filter.')
            return
        if not contacts:
            print('No more pages.')
            page -= 1
            continue
        print(f'Page {page + 1} ({len(contacts)} records)')
        display_contacts(contacts)
        action = input('[N]ext, [P]rev, [Q]uit: ').strip().lower()
        if action == 'n':
            page += 1
        elif action == 'p' and page > 0:
            page -= 1
        else:
            break


def search_contacts():
    query = input('Enter free-text search query: ').strip()
    if not query:
        print('Search query cannot be empty.')
        return
    results = connect.search_contacts(query)
    if not results:
        print('No results found.')
        return
    for row in results:
        print(f"[{row['contact_id']}] {row['first_name']} {row['last_name']} | {row['group_name'] or 'Other'} | {row['email'] or '-'}")
        print(f"    Phones: {row.get('phone_numbers', '-')}")
        print('-' * 80)


def search_by_email():
    query = input('Enter email search string: ').strip()
    if not query:
        print('Email search cannot be empty.')
        return
    page = 0
    while True:
        contacts = connect.select_contacts_with_filters(email_query=query, order_by='name', limit=PAGE_SIZE, offset=page * PAGE_SIZE)
        if not contacts and page == 0:
            print('No contacts found matching that email search.')
            return
        if not contacts:
            print('No more pages.')
            page -= 1
            continue
        print(f'Page {page + 1} ({len(contacts)} records)')
        display_contacts(contacts)
        action = input('[N]ext, [P]rev, [Q]uit: ').strip().lower()
        if action == 'n':
            page += 1
        elif action == 'p' and page > 0:
            page -= 1
        else:
            break


def add_phone():
    first = clean_text(input('Contact first name: '))
    last = clean_text(input('Contact last name: '))
    if not first or not last:
        print('Contact name is required.')
        return
    phone = clean_text(input('Phone number: '))
    if not phone:
        print('Phone number is required.')
        return
    phone_type = normalize_phone_type(input('Phone type (home/work/mobile): '))
    contact_name = first
    connect.add_phone_procedure(contact_name, phone, phone_type)
    print('Phone add request sent to database.')


def move_contact():
    first = clean_text(input('Contact first name: '))
    last = clean_text(input('Contact last name: '))
    if not first or not last:
        print('Contact name is required.')
        return
    group_name = normalize_group(input('New group name: '))
    if not group_name:
        print('Group name is required.')
        return
    connect.move_to_group_procedure(first, group_name)
    print(f'{first} moved to group {group_name}.')


def initialize_schema():
    connect.initialize_database()
    print('Database schema and groups are ready.')


def show_menu():
    print('\nPhoneBook Advanced Menu:')
    print('1) Initialize database schema and groups')
    print('2) Browse contacts (filter / sort / paginate)')
    print('3) Search all fields')
    print('4) Search by email')
    print('5) Export contacts to JSON')
    print('6) Import contacts from JSON')
    print('7) Import contacts from CSV')
    print('8) Add phone to contact')
    print('9) Move contact to group')
    print('0) Exit')


def main():
    while True:
        show_menu()
        choice = input('Choose an option: ').strip()
        if choice == '1':
            initialize_schema()
        elif choice == '2':
            browse_contacts()
        elif choice == '3':
            search_contacts()
        elif choice == '4':
            search_by_email()
        elif choice == '5':
            path = input(f'Export file [{DEFAULT_EXPORT_JSON}]: ').strip() or DEFAULT_EXPORT_JSON
            export_contacts_to_json(path)
        elif choice == '6':
            path = input(f'Import JSON file [{DEFAULT_IMPORT_JSON}]: ').strip() or DEFAULT_IMPORT_JSON
            import_contacts_from_json(path)
        elif choice == '7':
            path = input(f'Import CSV file [{DEFAULT_CSV}]: ').strip() or DEFAULT_CSV
            import_contacts_from_csv(path)
        elif choice == '8':
            add_phone()
        elif choice == '9':
            move_contact()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Unknown option, please try again.')
        press_enter_to_continue()


if __name__ == '__main__':
    main()
