# fetch GL_members from a csv file
import csv
from objects import GLMember

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

        print(f"{counter+1}: {ogrenci_adi} ({ogrenci_no})")

# fetch CARD informations from a csv file



