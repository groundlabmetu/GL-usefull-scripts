
class GLMember:
    def __init__(self, row_no:str = None, ogrenci_adi:str = None, girebilite:bool = None, ogrenci_no:str=None, giris_yili:str=None, tanitim:str=None, elektronik:str=None, atolye:str=None, printer:str=None, note:str=None):
        self.row_no = row_no
        self.ogrenci_adi = ogrenci_adi
        self.girebilite = girebilite
        self.ogrenci_no = ogrenci_no
        self.giris_yili = giris_yili
        self.tanitim = tanitim
        self.elektronik = elektronik
        self.atolye = atolye
        self.printer = printer
        self.note = note

        self.activehash = None
    
        self.student_hashes = []

    def append_hash(self, hash:str):
        self.student_hashes.append(hash)

    def set_active_hash(self):
        reversed_hash_list = self.student_hashes[::-1]
        for hash in reversed_hash_list:
            if not hash.is_zero_hash:
                self.activehash = hash
                break
        
            
                





    
class CardRequests():
    def __init__(self, zaman_damgasi:str=None, ad_soyad:str =None, ogrenci_no:str = None, hash:str=None, comments:str = None, is_zero_hash:bool = None):
        self.zaman_damgasi = zaman_damgasi
        self.ad_soyad = ad_soyad
        self.ogrenci_no = ogrenci_no
        self.hash = hash
        self.comments = comments
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




        