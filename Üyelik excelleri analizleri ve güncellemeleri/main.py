# fetch users from a csv file
import csv

GL_members = []

with open('Ground Lab Üyeler - Aktif üyeler.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        GL_members.append(row)
        print(row)