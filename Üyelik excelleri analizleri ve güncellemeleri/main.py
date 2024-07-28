# fetch users from a csv file
import csv
import 

GL_members = []

with open('Ground Lab Üyeler - Aktif üyeler.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
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

