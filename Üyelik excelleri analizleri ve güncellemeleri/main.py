
import csv, time
from objects import GLMember
from objects import CardRequests

PARAM_PRINT_ROWS = True

# fetch GL_members from a csv file ========================================
GL_members = []
with open('Ground Lab Üyeler - Aktif üyeler.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Ignore the first row
    for counter, row in enumerate(reader):
        row_no = row[0]
        ogrenci_adi = row[1]
        girebilite = row[2]
        ogrenci_no = row[3]
        giris_yili = row[4]
        tanitim = row[5]
        elektronik = row[6]
        atolye = row[7]
        printer = row[8]
        note = row[9]
        GL_members.append(GLMember(row_no, ogrenci_adi, girebilite, ogrenci_no, giris_yili, tanitim, elektronik, atolye, printer, note))

        if PARAM_PRINT_ROWS: print(f"{counter+1}: {ogrenci_adi} ({ogrenci_no})")

# Check if there is any duplicate student number in the GL_members
student_numbers = []
for member in GL_members:
    if member.ogrenci_no in student_numbers:
        print(f"Duplicate student number: {member.ogrenci_adi} - ({member.ogrenci_no})")
        raise Exception("Duplicate student number")
    else:
        student_numbers.append(member.ogrenci_no)


# fetch CARD informations from a csv file ========================================
card_requests = []
with open('Masa kullanımı ile ilgili request (Yanıtlar) - Form Yanıtları 1.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Ignore the first row
    for counter, row in enumerate(reader):
        zaman_damgasi = row[0]
        ad_soyad = row[1]
        ogrenci_no = row[2]
        hash = row[3]
        comments = row[4]

        is_zero_hash = (hash == "$argon2id$v=19$m=2097152__t=2__p=4$2p4gW1kQc3+daOMV7G50NA$SBS9Uwsa+TJOskYOkx1lYrGbePpIEy/XVlz3ZfDvDGY")
        card_requests.append(CardRequests(zaman_damgasi, ad_soyad, ogrenci_no, hash, comments, is_zero_hash))
        if PARAM_PRINT_ROWS: card_requests[-1].print_object(counter+1)

# MATCH CARDS WITH PERSON ========================================

for member in GL_members:
    for card in card_requests:
        if member.ogrenci_no == card.ogrenci_no:
            member.append_hash(card)

#WHICH ONE IS ACTIVE HASH
for member in GL_members:
    member.set_active_hash()

# PRINT THE RESULT ========================================
for counter, member in enumerate(GL_members):
    is_hash_assigned = member.activehash is not None
    print(f"{counter}| {member.ogrenci_adi:<{30}} - ({member.ogrenci_no:<{15}}) -> Hash atandı: {is_hash_assigned:<{7}} | Hash sayısı: {len(member.student_hashes):<{5}}")

    

Student = []
with open('Students - Sayfa1.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Ignore the first row
    for counter, row in enumerate(reader):
        ad_soyad = row[0]
        ogrenci_no = row[1]
        hash = row[2]
        mechanics = row[3]
        electronics_1 = row[4]
        electronics_2 = row[5]
        printer = row[6]
        Student.append(GLMember(ad_soyad, ogrenci_no, hash, mechanics, electronics_1, electronics_2, printer))