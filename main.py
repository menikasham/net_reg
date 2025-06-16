import re
from pprint import pprint
import csv


pattern = re.compile(r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})')
pattern_ext = re.compile(r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})(доб\.\d{4})')
pattern_2 = re.compile(r"^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$")

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_list = contacts_list[1::]
# pprint(contacts_list)

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



for item in contacts_list:
    fio = split_fio(item[:3])
    fio.extend(item[3:])
    fio[-2] = re.sub(" |[()]|-", "", fio[-2])
    fio[-2] = re.sub(r"^8", "+7", fio[-2])
    fio[-2] = re.sub(r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})(доб\.\d{4})', r'\1(\2)\3-\4-\5 \6', fio[-2])
    fio[-2] = re.sub(r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})', r'\1(\2)\3-\4-\5', fio[-2])

    print(fio)




# with open("phonebook.csv", "w", encoding="utf-8") as f:
#   datawriter = csv.writer(f, delimiter=',')
#   datawriter.writerow(['lastname','firstname','surname','organization','position','phone','email'])
#   # Вместо contacts_list подставьте свой список
#   datawriter.writerows(contacts_list)

