import re
import csv
from collections import defaultdict

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_list = contacts_list[1::]
addr_book = []


def split_fio(raw: list):
    if raw[0] and raw[1] and raw[2]:
        return raw
    elif len(raw[0].split(" ")) == 3:
        outer_list = raw[0].split(" ")
        return outer_list
    elif len(raw[1].split(" ")) == 2:
        outer_list = raw[1].split(" ")
        outer_list.insert(0, raw[0])
        return outer_list
    elif len(raw[0].split(" ")) == 2:
        outer_list = raw[0].split(" ")
        outer_list.insert(2, raw[2])
        return outer_list


def merge_contacts(contacts):
    grouped = defaultdict(list)
    for contact in contacts:
        key = f"{contact['lastname']} {contact['firstname']}"
        grouped[key].append(contact)

    merged = []
    for key, group in grouped.items():
        position = set()
        phone = set()
        email = set()
        for pos in group:
            position.update(pos.get('position', []))
        for ph in group:
            phone.update(ph.get('phone', []))
        for em in group:
            email.update(em.get('email', []))
        merged_contact = group[0]
        merged_contact['position'] = "".join(list(position))
        merged_contact['phone'] = "".join(list(phone))
        merged_contact['email'] = "".join(list(email))
        merged.append(merged_contact)

    return merged


for item in contacts_list:
    fio = split_fio(item[:3])
    fio.extend(item[3:])
    fio[-2] = re.sub(" |[()]|-", "", fio[-2])
    fio[-2] = re.sub(r"^8|^7", "+7", fio[-2])
    fio[-2] = re.sub(r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})(доб\.\d{4})', r'\1(\2)\3-\4-\5 \6', fio[-2])
    fio[-2] = re.sub(r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})', r'\1(\2)\3-\4-\5', fio[-2])

    addr_book.append({
        'lastname': fio[0],
        'firstname': fio[1],
        'surname': fio[2],
        'organization': fio[3],
        'position': [fio[4]],
        'phone': [fio[5]],
        'email': [fio[6]]
    })

result = merge_contacts(addr_book)

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email'])
    for res in result:
        datawriter.writerow([res['lastname'], res['firstname'], res['surname'], res['organization'],
                             res['position'], res['phone'], res['email']])
