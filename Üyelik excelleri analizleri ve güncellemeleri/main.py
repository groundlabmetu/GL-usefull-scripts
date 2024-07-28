
import csv, time
from objects import GLMember
from objects import CardRequests
from objects import Students

PARAM_PRINT_GL_MEMBERS = False
PARAM_PRINT_CARD_REQUESTS = False
PARAM_PRINT_HASH_ASSIGNMENTS = False
PARAM_PRINT_STUDENTS = False

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

        if PARAM_PRINT_GL_MEMBERS: GL_members[-1].print_object(counter)

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

        if PARAM_PRINT_CARD_REQUESTS: card_requests[-1].print_object(counter)

# MATCH CARDS WITH PERSON ========================================
for member in GL_members:
    for card in card_requests:
        if member.ogrenci_no == card.ogrenci_no:
            member.append_hash(card)

#WHICH ONE IS ACTIVE HASH
for member in GL_members:
    member.set_active_hash()

# PRINT THE RESULT ========================================
if PARAM_PRINT_HASH_ASSIGNMENTS:
    for counter, member in enumerate(GL_members):
        is_hash_assigned = member.activehash is not None
        print(f"{counter}| {member.ogrenci_adi:<{30}} - ({member.ogrenci_no:<{15}}) -> Hash atandı: {is_hash_assigned:<{7}} | Hash sayısı: {len(member.student_hashes):<{5}}")

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

        if PARAM_PRINT_STUDENTS: students[-1].print_object()

# Update 'Students' list
for GL_member in GL_members:
    if GL_member.girebilite == False: continue
    if GL_member.activehash is None: continue

    for student in students: # If the student is in the GL_members list, update the student's hash
        if GL_member.ogrenci_no == student.ogrenci_no:
            student.hash = GL_member.activehash.hash

            if student.mechanics != GL_member.return_mechanic_time():
                print(f"{'      (Updated Student):':<{50}}Mechanic time is updated for {student.ad_soyad} from {student.mechanics} to {GL_member.return_mechanic_time()}")
                student.mechanics = GL_member.return_mechanic_time()

            if student.electronics_1 != GL_member.return_electronics_1_time():
                print(f"{'      (Updated Student):':<{50}}Electronics 1 time is updated for {student.ad_soyad} from {student.electronics_1} to {GL_member.return_electronics_1_time()}")
                student.electronics_1 = GL_member.return_electronics_1_time()

            if student.electronics_2 != GL_member.return_electronics_2_time():
                print(f"{'      (Updated Student):':<{50}}Electronics 2 time is updated for {student.ad_soyad} from {student.electronics_2} to {GL_member.return_electronics_2_time()}")
                student.electronics_2 = GL_member.return_electronics_2_time()
            
            if student.printer != GL_member.return_printer_time():
                print(f"{'      (Updated Student):':<{50}}Printer time is updated for {student.ad_soyad} from {student.printer} to {GL_member.return_printer_time()}")
                student.printer = GL_member.return_printer_time()

            break

    else:
        new_student = Students(GL_member.ogrenci_adi, GL_member.ogrenci_no, GL_member.activehash.hash, GL_member.return_mechanic_time(), GL_member.return_electronics_1_time(), GL_member.return_electronics_2_time(), GL_member.return_printer_time())
        students.append(new_student)

        print(f"{'(New Students):':<{50}}{new_student.ad_soyad:<{30}} - ({new_student.ogrenci_no:<{15}}), ($hash), {new_student.mechanics:<{4}}, {new_student.electronics_1:<{4}}, {new_student.electronics_2:<{4}}, {new_student.printer:<{4}}")
                
