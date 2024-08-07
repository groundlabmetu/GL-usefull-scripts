import string

class CardRequests():
    def __init__(self, zaman_damgasi:str=None, ad_soyad:str =None, ogrenci_no:str = None, hash:str=None, comments:str = None, is_zero_hash:bool = None):
        self.zaman_damgasi = zaman_damgasi
        self.ad_soyad = ad_soyad
        self.ogrenci_no = ogrenci_no       
        self.comments = comments
        self.hash = hash
        self.is_zero_hash = is_zero_hash

    def print_object(self, counter:int):
        print()
        print(f"{counter}:")
        print(f"zaman_damgasi: {self.zaman_damgasi}")
        print(f"ad_soyad: {self.ad_soyad}")
        print(f"ogrenci_no: {self.ogrenci_no}")
        print(f"hash: {self.hash}")
        print(f"comments: {self.comments}")
        print(f"is_zero_hash: {self.is_zero_hash}")
        print()

class Students():
    def __init__(self, ad_soyad:str=None, ogrenci_no:str =None, hash:str = None, mechanics:str=None, electronics_1:str = None, electronics_2:str = None, printer:str = None):
        self.ad_soyad = ad_soyad
        self.ogrenci_no = ogrenci_no
        self.hash = hash
        self.mechanics = mechanics
        self.electronics_1 = electronics_1
        self.electronics_2 = electronics_2
        self.printer = printer
      
    def print_object(self):
        print()
        print(f"ad_soyad: {self.ad_soyad}")
        print(f"ogrenci_no: {self.ogrenci_no}")
        print(f"hash: {self.hash}")
        print(f"mechanics: {self.mechanics}")
        print(f"electronics_1: {self.electronics_1}")
        print(f"electronics_2: {self.electronics_2}")
        print(f"printer: {self.printer}")
        print()

    def translate_name_to_english(self):
        turkish_to_english = str.maketrans(
        "çÇğĞıİöÖşŞüÜ",
        "cCgGiIoOsSuU"
        )
        translated_text = self.ad_soyad.translate(turkish_to_english)
        english_chars = string.ascii_letters + string.whitespace
        filtered_text = ''.join([char for char in translated_text if char in english_chars])
        self.ad_soyad = filtered_text.upper()

    def update_durations(self, mechanic_duration:str, electronics_1_duration:str, electronics_2_duration:str, printer_duration:str):
        self.mechanics = mechanic_duration if self.mechanics != "0" else "0"
        self.electronics_1 = electronics_1_duration if self.electronics_1 != "0" else "0"
        self.electronics_2 = electronics_2_duration if self.electronics_2 != "0" else "0"
        self.printer = printer_duration if self.printer != "0" else "0"

class GLMember:
    def __init__(self, row_no:str = None, ogrenci_adi:str = None, girebilite:bool = None, ogrenci_no:str=None,bolum:str =None, giris_yili:str=None, tanitim:str=None, elektronik:str=None, atolye:str=None, printer:str=None, note:str=None):
        self.row_no = row_no
        self.ogrenci_adi = ogrenci_adi
        self.girebilite = True if girebilite == "Girebilir" else False
        self.ogrenci_no = ogrenci_no
        self.bolum = bolum
        self.giris_yili = giris_yili
        self.tanitim = tanitim
        self.elektronik = elektronik
        self.atolye = atolye
        self.printer = printer
        self.note = note

        self.activehash = None
    
        self.student_hashes = []

    def print_object(self, counter:int):
        print()
        print(f"{counter}:")
        print(f"row_no: {self.row_no}")
        print(f"ogrenci_adi: {self.ogrenci_adi}")
        print(f"girebilite: {self.girebilite}")
        print(f"ogrenci_no: {self.ogrenci_no}")
        print(f"bolum: {self.bolum}")
        print(f"giris_yili: {self.giris_yili}")
        print(f"tanitim: {self.tanitim}")
        print(f"elektronik: {self.elektronik}")
        print(f"atolye: {self.atolye}")
        print(f"printer: {self.printer}")
        print(f"note: {self.note}")
        print(f"activehash: {self.activehash}")
        print(f"student_hashes: {self.student_hashes}")
        print()

    def append_hash(self, hash:str):
        self.student_hashes.append(hash)

    def set_active_hash(self):
        reversed_hash_list = self.student_hashes[::-1]
        for hash in reversed_hash_list:
            if not hash.is_zero_hash:
                self.activehash = hash
                break
          
    def return_info_excell_row(self, counter:int, student:Students = None, zero_hash:str = None):
        yetki_durumu = "Girebilir" if self.girebilite else "Yetki İptali"
        tanitim  = "Aldı" if len(self.tanitim) > 0 else "Almadı"
        elektronik = "Aldı" if len(self.elektronik) > 0 else "Almadı"
        atolye = "Aldı" if len(self.atolye) > 0 else "Almadı"
        printer = "Aldı" if len(self.printer) > 0 else "Almadı"
        kart_tanimli_mi = ""
        if student is not None:
            kart_tanimli_mi = "Kart Tanımlı"
        elif self.activehash is not None:
            kart_tanimli_mi = "Kart Tanımlı"
        elif len(self.student_hashes) > 0:
            kart_tanimli_mi = "Kart '0' Tanımlı, yeniden başvurunuz"
        else:
            kart_tanimli_mi = "Başvuruda Bulunulmamış"
        
        row_text = f"{counter}\t{self.ogrenci_no}\t{yetki_durumu}\t{tanitim}\t{elektronik}\t{atolye}\t{printer}\t{kart_tanimli_mi}\n"
        return row_text
    
    def return_mechanic_time(self, duration:str = "120"):
        return "0" if len(self.atolye)==0 else duration
    
    def return_electronics_1_time(self, duration:str = "120"):
        return "0" if len(self.elektronik)==0 else duration
    
    def return_electronics_2_time(self, duration:str = "120"):
        return "0" if len(self.elektronik)==0 else duration
    
    def return_printer_time(self, duration:str = "180"):
        return "0" if len(self.printer)==0 else duration
    
