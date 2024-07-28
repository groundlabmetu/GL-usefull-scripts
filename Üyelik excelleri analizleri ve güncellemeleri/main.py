import pyperclip
import csv, time
from objects import GLMember
from objects import CardRequests
from objects import Students

PARAM_PRINT_GL_MEMBERS_IMPORT = False
PARAM_PRINT_CARD_REQUESTS_IMPORT = False
PARAM_PRINT_STUDENT_IMPORT = False
PARAM_PRINT_STUDENT_CRUD = False
PARAM_PRINT_HASH_ASSIGNMENTS = False
PARAM_PRINT_COPY_TO_CLIPBOARD = False

PARAM_COPY_TO_CLIPBOARD = False

PARAM_MECHANIC_DURATION = "120"
PARAM_ELECTRONICS_1_DURATION = "120"
PARAM_ELECTRONICS_2_DURATION = "120"
PARAM_PRINTER_DURATION = "180"

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
        bolum = row[4]
        giris_yili = row[5]
        tanitim = row[6]
        elektronik = row[7]
        atolye = row[8]
        printer = row[9]
        note = row[10]
        GL_members.append(GLMember(row_no, ogrenci_adi, girebilite, ogrenci_no, bolum, giris_yili, tanitim, elektronik, atolye, printer, note))

        if PARAM_PRINT_GL_MEMBERS_IMPORT: GL_members[-1].print_object(counter)

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

        # check hash format validity
        argon_index = hash.find('$argon')
        if argon_index != -1:
            hash = hash[argon_index:]
        else:
            if PARAM_PRINT_CARD_REQUESTS_IMPORT: print(f"{counter:<5}| Skipping this CARD request, Hash does not containt '$argon': {hash}")
            continue    

        if len(hash) > 101:
            hash = hash[:101]
        elif len(hash) < 101:
            if PARAM_PRINT_CARD_REQUESTS_IMPORT: print(f"{counter:<5}| Skipping this CARD request,Hash is shorter than 101 characters: {hash}")
            continue
            
        if PARAM_PRINT_CARD_REQUESTS_IMPORT: print(f"{counter:<5}| Hash: {hash}")
        is_zero_hash = (hash == "$argon2id$v=19$m=2097152__t=2__p=4$2p4gW1kQc3+daOMV7G50NA$SBS9Uwsa+TJOskYOkx1lYrGbePpIEy/XVlz3ZfDvDGY")
        card_requests.append(CardRequests(zaman_damgasi, ad_soyad, ogrenci_no, hash, comments, is_zero_hash))

        if PARAM_PRINT_CARD_REQUESTS_IMPORT: card_requests[-1].print_object(counter)

# math the card requests with the GL_members ========================================
for member in GL_members:
    for card in card_requests:
        if member.ogrenci_no == card.ogrenci_no:
            member.append_hash(card)

# Decide on the active hash for each member ========================================
for member in GL_members:
    member.set_active_hash()

students = []
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
        students.append(Students(ad_soyad, ogrenci_no, hash, mechanics, electronics_1, electronics_2, printer))  

        if PARAM_PRINT_STUDENT_IMPORT: students[-1].print_object()

# CRUD 'Students' list
if PARAM_PRINT_STUDENT_CRUD: print("Printing student CRUD operations:")
for GL_member in GL_members:
    if GL_member.girebilite == False: continue
    if GL_member.activehash is None: continue

    for student in students:
        if GL_member.ogrenci_no == student.ogrenci_no:
            student.hash = GL_member.activehash.hash

            updates = []

            if student.mechanics != GL_member.return_mechanic_time(duration = PARAM_MECHANIC_DURATION):
                updates.append(f"Mechanic {student.mechanics}->{GL_member.return_mechanic_time(duration = PARAM_MECHANIC_DURATION)}")
                student.mechanics = GL_member.return_mechanic_time(duration = PARAM_MECHANIC_DURATION)

            if student.electronics_1 != GL_member.return_electronics_1_time(duration = PARAM_ELECTRONICS_1_DURATION):
                updates.append(f"Electronics 1 {student.electronics_1}->{GL_member.return_electronics_1_time(duration = PARAM_ELECTRONICS_1_DURATION)}")
                student.electronics_1 = GL_member.return_electronics_1_time(duration = PARAM_ELECTRONICS_1_DURATION)

            if student.electronics_2 != GL_member.return_electronics_2_time(duration = PARAM_ELECTRONICS_2_DURATION):
                updates.append(f"Electronics 2 {student.electronics_2}->{GL_member.return_electronics_2_time(duration = PARAM_ELECTRONICS_2_DURATION)}")
                student.electronics_2 = GL_member.return_electronics_2_time(duration = PARAM_ELECTRONICS_2_DURATION)
            
            if student.printer != GL_member.return_printer_time(duration = PARAM_PRINTER_DURATION):
                updates.append(f"Printer {student.printer}->{GL_member.return_printer_time(duration = PARAM_PRINTER_DURATION)}")
                student.printer = GL_member.return_printer_time(duration = PARAM_PRINTER_DURATION)


            if PARAM_PRINT_STUDENT_CRUD and len(updates) > 0:
                print(f"{'      (Updated Student): '+student.ad_soyad:<{50}}{', '.join(updates)}")

            break

    else:
        new_student = Students(GL_member.ogrenci_adi, GL_member.ogrenci_no, GL_member.activehash.hash, GL_member.return_mechanic_time(duration = PARAM_MECHANIC_DURATION), GL_member.return_electronics_1_time(duration = PARAM_ELECTRONICS_1_DURATION), GL_member.return_electronics_2_time(duration = PARAM_ELECTRONICS_2_DURATION), GL_member.return_printer_time(duration = PARAM_PRINTER_DURATION))
        students.append(new_student)

        if PARAM_PRINT_STUDENT_CRUD: print(f"{'(New Students):':<{50}}{new_student.ad_soyad:<{30}} - ({new_student.ogrenci_no:<{15}}), ($hash), {new_student.mechanics:<{4}}, {new_student.electronics_1:<{4}}, {new_student.electronics_2:<{4}}, {new_student.printer:<{4}}")

# Ensure that student names are english characters
for student in students:
    student.translate_name_to_english()

# Ensure that previous students durations are updated
for student in students:
    student.update_durations(
        mechanic_duration= PARAM_MECHANIC_DURATION, 
        electronics_1_duration= PARAM_ELECTRONICS_1_DURATION, 
        electronics_2_duration= PARAM_ELECTRONICS_2_DURATION, 
        printer_duration= PARAM_PRINTER_DURATION
    )

if PARAM_PRINT_HASH_ASSIGNMENTS:
    for counter, member in enumerate(GL_members):
        is_hash_assigned = member.activehash is not None
        gecerli_hash_text = "YOK" if is_hash_assigned else "VAR"
        print(f"{counter:<{4}}| {member.ogrenci_adi:<{30}} {member.ogrenci_no:<{15}} -> Hash: {gecerli_hash_text:<{7}} | Hash basvuru sayısı: {len(member.student_hashes):<{5}}")

# Ensure that student 
# copy the updated 'Students' list to clipboard ========================================

pyperclip.copy("ad_soyad \t ogrenci_no,hash,mechanics,electronics_1,electronics_2,printer\n")

string_to_copy = ""
if PARAM_PRINT_COPY_TO_CLIPBOARD: print(f"{'NO':<4}|{'AD-SOYAD':<30}{'S-NO':<10}{'HASH':<40}{'MEKANIK':<15}{'ELEKTRONIK1':<15}{'ELEKTRONIK2':<15}{'PRINTER':<15}")
for counter, student in enumerate(students):
    string_to_copy += f"{student.ad_soyad}\t{student.ogrenci_no}\t{student.hash}\t{student.mechanics}\t{student.electronics_1}\t{student.electronics_2}\t{student.printer}\n"
    if PARAM_PRINT_COPY_TO_CLIPBOARD: print(f"{counter:<4}|{student.ad_soyad:<30}{student.ogrenci_no:<10}{student.hash[:6] +'...'+ student.hash[-26:]:<40}{student.mechanics:<15}{student.electronics_1:<15}{student.electronics_2:<15}{student.printer:<15}")

if PARAM_COPY_TO_CLIPBOARD:
    print("Copying to clipboard...")
    pyperclip.copy(string_to_copy)

string_to_copy = ""
for counter, GL_member in enumerate(GL_members):
    matched_student = None
    for student in students:
        if GL_member.ogrenci_no == student.ogrenci_no:
            if student.hash != "$argon2id$v=19$m=2097152__t=2__p=4$2p4gW1kQc3+daOMV7G50NA$SBS9Uwsa+TJOskYOkx1lYrGbePpIEy/XVlz3ZfDvDGY":
                matched_student = student
                break                
    
    string_to_copy += GL_member.return_info_excell_row(counter = counter+1, student = matched_student)

           



print("Copying to clipboard...")
pyperclip.copy(string_to_copy)