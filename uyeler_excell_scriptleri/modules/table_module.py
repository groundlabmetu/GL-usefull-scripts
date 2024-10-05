from pathlib import Path
import pprint
import pyperclip
import unicodedata
import re

class MemberTable:

    def __init__(self, member_table_path: Path = None):
        self.member_table_path = member_table_path
        self.member_table_rows = []  # Each row is parsed to a dictionary 
        ####
        # {
        #    row_no: str,
        #    ogrenci_adi: str,
        #    girebilite: bool,
        #    bolum: str,
        #    giris_yili: str,
        #    tanitim: str,
        #    elektronik: str,
        #    atolye: str,
        #    yazici: str,
        #    not: str
        # }
        ####

        self.init_member_table_rows()

    def init_member_table_rows(self):    
        print("[INFO] Initializing member table rows...")    
        string_rows = []
        with open(self.member_table_path, 'r', encoding='utf-8') as f:
            string_rows = f.readlines()

        # Parse each row to a dictionary
        self.member_table_rows = []
        for row in string_rows:
            splited_row = row.strip().split(',')
            row_dict = {}
            row_dict['row_no'] = splited_row[0]
            row_dict['ogrenci_adi'] = splited_row[1]
            row_dict['girebilite'] = splited_row[2]
            row_dict['ogrenci_no'] = splited_row[3]
            row_dict['bolum'] = splited_row[4]
            row_dict['giris_yili'] = splited_row[5]
            row_dict['tanitim'] = splited_row[6]
            row_dict['elektronik'] = splited_row[7]
            row_dict['atolye'] = splited_row[8]
            row_dict['yazici'] = splited_row[9]
            row_dict['not'] = splited_row[10]

            self.member_table_rows.append(row_dict)
            
        #pop first row since it is the header
        self.member_table_rows.pop(0)

    def validate_each_row_has_unique_and_numeric_row_no(self):
        print("[INFO] Validating each row has unique row_no...")
        row_no_list = []
        for row in self.member_table_rows:
            if row['row_no'].isnumeric() == False:
                raise Exception(f"row_no is not numeric: {row['row_no']}\nRow details:\n{pprint.pformat(row)}")
            if row['row_no'] in row_no_list:
                raise Exception(f"Duplicate row_no: {row['row_no']}\nRow details:\n{pprint.pformat(row)}")
            else:
                row_no_list.append(row['row_no'])

    def validate_each_row_has_unique_and_numeric_student_no(self):
        print("[INFO] Validating each row has unique and numeric student_no...")
        student_no_list = []
        for row in self.member_table_rows:
            if row['ogrenci_no'].isnumeric() == False:
                raise Exception(f"ogrenci_no is not numeric: {row['ogrenci_no']}\nRow details:\n{pprint.pformat(row)}")
            if row['ogrenci_no'] in student_no_list:
                raise Exception(f"Duplicate student_no: {row['ogrenci_no']} - {row['ogrenci_adi']}\nRow details:\n{pprint.pformat(row)}")
            else:
                student_no_list.append(row['ogrenci_no'])

    def warn_if_multiple_rows_have_the_same_student_name(self):
        print("[INFO] Warning if multiple rows have the same student name...")
        student_name_list = []
        for row in self.member_table_rows:
            if row['ogrenci_adi'] in student_name_list:
                print(f"\tMultiple rows with name: {row['ogrenci_adi']}")
            else:
                student_name_list.append(row['ogrenci_adi'])

    def validate_yazici_authorization_if_elektronik_is_available(self):
        # Eğer birisinin elektronik yetkisi varsa yazıcı yetkisi de olmalı.
        print("[INFO] Validating yazici authorization if elektronik is available...")
        for row in self.member_table_rows:
            if row['elektronik'] != '' and row['yazici'] == '':
                raise Exception(f"Elektronik is available but yazici is not authorized: {row['ogrenci_adi']}\nRow details:\n{pprint.pformat(row)}")

    def validate_name_format(self):
        #All uppercase english characters
        allowed_chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZ()-"
        for row in self.member_table_rows:            
            for char in row['ogrenci_adi']:
                if char not in allowed_chars:
                    raise Exception(f"Name format is not valid: {row['ogrenci_adi']}\nRow details:\n{pprint.pformat(row)}")          
            
    def validate_member_table(self):
        self.validate_each_row_has_unique_and_numeric_row_no()
        self.validate_each_row_has_unique_and_numeric_student_no()
        self.warn_if_multiple_rows_have_the_same_student_name()
        self.validate_yazici_authorization_if_elektronik_is_available()
        self.validate_name_format()

    def get_member_table_rows(self):
        return self.member_table_rows

    def format_and_copy_student_names_to_clipboard(self):
        self.init_member_table_rows()

        student_names = [row['ogrenci_adi'] for row in self.member_table_rows]

        # Define the character mapping
        char_map = {
            "ç": "C",
            "Ç": "C",
            "ğ": "G",
            "Ğ": "G",
            "ı": "I",
            "i": "I",
            "İ": "I",
            "İ": "I",
            "ö": "O",
            "Ö": "O",
            "ş": "S",
            "Ş": "S",
            "ü": "U",
            "Ü": "U"
        }

        for i in range(len(student_names)):
            student_name = student_names[i]
            # Normalize the string to NFC form to standardize character representations
            student_name_upper = unicodedata.normalize('NFC', student_name.upper())
            # Replace characters using the mapping
            for key, value in char_map.items():
                student_name_upper = student_name_upper.replace(key, value)
            student_names[i] = student_name_upper
            print(f"Original name: {student_name} - Translated name: {student_name_upper}")

        student_names = '\n'.join(student_names)
        pyperclip.copy(student_names)
        print("[INFO] Student names are copied to clipboard.")

class CardRequestsTable:
    
    def __init__(self, member_table_path: Path = None):
        self.card_request_table_csv_path = member_table_path
        self.card_request_table_rows = []  # Each row is parsed to a dictionary 
        ####
        # {
        #    timestamp: str,
        #    ad_soyad: str,
        #    student_no: str,
        #    argon_hash: str,
        # }
        ####
        self.init_card_requests_table_rows()

    def init_card_requests_table_rows(self):
        print("[INFO] Initializing card requests table rows...")
        with open(self.card_request_table_csv_path, 'r', encoding='utf-8') as f:
            string_rows = f.readlines()

        # Parse each row to a dictionary
        t_list = []
        for row in string_rows:
            splited_row = row.strip().split(',')
            row_dict = {}
            row_dict['timestamp'] = splited_row[0]
            row_dict['ad_soyad'] = splited_row[1].lower()
            row_dict['student_no'] = splited_row[2]
            row_dict['argon_hash'] = splited_row[3]
            t_list.append(row_dict)

        #pop first row since it is the header
        t_list.pop(0)

        #Check for argon hash format and zero-id card hash, then add row to the list
        self.card_request_table_rows = []
        argon_key_pattern = r'\$argon2id\$v=\d+\$m=\d+__t=\d+__p=\d+\$[A-Za-z0-9+/]+={0,2}\$[A-Za-z0-9+/]+={0,2}'
        for row_dict in t_list:
            argon_hash_input = row_dict['argon_hash']
            match = re.search(argon_key_pattern, argon_hash_input)
            if match:
                row_dict['argon_hash'] = match.group(0)
            else:
                print(f"\tArgon hash is not in the correct format: {row_dict['ad_soyad']} - {row_dict['student_no']} : {row_dict['argon_hash']}")
                continue

            #check if hash corresponding to zero-id card (i.e. no card present)
            if  row_dict['argon_hash'] == "$argon2id$v=19$m=2097152__t=2__p=4$2p4gW1kQc3+daOMV7G50NA$SBS9Uwsa+TJOskYOkx1lYrGbePpIEy/XVlz3ZfDvDGY":
                print(f"\tZero-id card hash: {row_dict['ad_soyad']} - {row_dict['student_no']} : {row_dict['argon_hash']}")
                continue

            self.card_request_table_rows.append(row_dict)

    def get_card_requests_table_rows(self):
        return self.card_request_table_rows # [{timestamp, ad_soyad, student_no, argon_hash}]

class APITable:

    def __init__(self, member_table_rows: list[dict] = None, card_requests_table_rows: list[dict] = None, mechanic_minutes: int = 120, electronics_1_minutes: int = 120, electronics_2_minutes: int = 120, printer_minutes: int = 240):
        self.member_table_rows = member_table_rows
        self.card_requests_table_rows = card_requests_table_rows

        self.mechanic_minutes = int(mechanic_minutes)
        self.electronics_1_minutes = int(electronics_1_minutes)
        self.electronics_2_minutes = int(electronics_2_minutes)
        self.printer_minutes = int(printer_minutes)

        self.api_table_rows = []        
        ####
        # {
        #    name: str,
        #    student_id: str,
        #    card_id: bool,
        #    mechanics: str,
        #    electronic_1: str,
        #    electronic_2: str,
        #    printer: str,
        # }
        ####

    def create_api_table(self):
        print("[INFO] Creating API table...")

        self.api_table_rows = []
        #iterate over each member in the member table and try to match with the card request table
        for member in self.member_table_rows:
            student_no = member['ogrenci_no']
            # find the newest card request for the student_no in the card request table and match it with the member
            for card_request in reversed(self.card_requests_table_rows):
                if student_no == card_request['student_no']:
                    api_table_row = {}
                    api_table_row['name'] = member['ogrenci_adi']
                    api_table_row['student_id'] = student_no
                    api_table_row['card_id'] = card_request['argon_hash']
                    api_table_row['mechanics'] = self.mechanic_minutes if member['atolye'] != "" else "0"
                    api_table_row['electronic_1'] = self.electronics_1_minutes if member['elektronik'] != "" else "0"
                    api_table_row['electronic_2'] = self.electronics_2_minutes if member['elektronik'] != "" else "0"
                    api_table_row['printer'] = self.printer_minutes  if member['yazici'] != "" else "0"
                    self.api_table_rows.append(api_table_row)
                    break

        #Order the table by name
        self.api_table_rows = sorted(self.api_table_rows, key=lambda x: x['name'])

    def copy_api_table_to_clipboard(self):
        api_table_str = ""
        for row in self.api_table_rows:
            api_table_str += f"{row['name']}\t{row['student_id']}\t{row['card_id']}\t{row['mechanics']}\t{row['electronic_1']}\t{row['electronic_2']}\t{row['printer']}\n"

        answer = input("Do you want to copy the API table to clipboard? (y/n): ")
        if answer.lower() == "y":
            pyperclip.copy(api_table_str)
            print("[INFO] API table is copied to clipboard.")        

    def get_api_table_rows(self):
        return self.api_table_rows
    
class InformationTable:
    def __init__(self, member_table_rows:list[dict] = None, api_table_rows:list[dict] = None):
        self.member_table_rows = member_table_rows
        self.api_table_rows = api_table_rows

        self.information_table_rows = [] # [{name, is_banned_info, student_id, is_card_registered, mechanics, electronic_1, electronic_2, printer}]

    def create_information_table(self):
        self.information_table_rows = []  
        for member in self.member_table_rows:
            student_no = member['ogrenci_no']
            information_table_row = {
                'name': ' '.join([word[0] + '*' * (len(word) - 1) for word in member['ogrenci_adi'].split()]),
                'is_banned_info': member['girebilite'],
                'student_id': int(student_no),
                'is_card_registered': "Kartı Tanımlı" if any(api_row['student_id'] == student_no for api_row in self.api_table_rows) else "Kartı Tanımlı Değil",
                'tanitim': "Tanıtım Var" if member['tanitim'] != "" else "-",
                'mechanics': "Atölye Var" if member['atolye'] != "" else "-",                
                'electronic': "Elektronik Var" if member['elektronik'] != "" else "-",
                'printer': "3D Yazıcı Var" if member['yazici'] != "" else "-"
            }
           
            self.information_table_rows.append(information_table_row)

        #order wrt student no
        self.information_table_rows = sorted(self.information_table_rows, key=lambda x: x['student_id'])

    def copy_information_table_to_clipboard(self):
        information_table_str = ""
        for row in self.information_table_rows:
            #student no, name, is_banned_info, is_card_registered, tanitim, electronic_1, electronic_2, printer, mechanics
            information_table_str += f"{row['student_id']}\t{row['name']}\t{row['is_banned_info']}\t{row['is_card_registered']}\t{row['tanitim']}\t{row['electronic']}\t{row['printer']}\t{row['mechanics']}\n"

        answer = input("Do you want to copy the Information table to clipboard? (y/n): ")
        if answer.lower() == "y":
            pyperclip.copy(information_table_str)
            print("[INFO] Information table is copied to clipboard.")
        
if __name__ == "__main__":
    csv_folder_path = Path(__file__).parent.parent.resolve() / 'csv_files'
    member_table_path = csv_folder_path / 'Ground Lab Üyeler - Aktif üyeler.csv'
    card_requests_table_path = csv_folder_path / 'Masa kullanımı ile ilgili request (Yanıtlar) - Form Yanıtları 1.csv'

    member_table_manager = MemberTable(member_table_path)
    member_table_manager.validate_member_table()

    card_requests_table_manager = CardRequestsTable(card_requests_table_path)

    api_table_manager = APITable(
        member_table_rows = member_table_manager.get_member_table_rows(),
        card_requests_table_rows = card_requests_table_manager.get_card_requests_table_rows(), 
        mechanic_minutes = 120, 
        electronics_1_minutes = 120, 
        electronics_2_minutes = 120, 
        printer_minutes = 240
    )
    api_table_manager.create_api_table()
    api_table_manager.copy_api_table_to_clipboard()
    