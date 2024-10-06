from pathlib import Path
from modules import pdf_module, table_module
import datetime, locale

#import csv files for GL members and card requests
csv_folder_path = Path(__file__).parent.resolve() / 'csv_files'
member_table_path = csv_folder_path / 'Ground Lab Üyeler - Aktif üyeler.csv'
card_requests_table_path = csv_folder_path / 'Masa kullanımı ile ilgili request (Yanıtlar) - Form Yanıtları 1.csv'

member_table_manager = table_module.MemberTable(member_table_path)
card_requests_table_manager = table_module.CardRequestsTable(card_requests_table_path) # Ignores zero hashes and matches key üsing regex. If any student has more than one request, the last request is taken. Corrupt request are ignored
member_table_manager.validate_member_table() # Ensures the table is in the correct format. Otherwise, it raises an exception.

# Create the API table using the member and card requests tables. API table is the one which governs who can acces the tables in the lab for how long.
api_table_manager = table_module.APITable(
    member_table_rows = member_table_manager.get_member_table_rows(),
    card_requests_table_rows = card_requests_table_manager.get_card_requests_table_rows(), 
    mechanic_minutes = 120, 
    electronics_1_minutes = 120, 
    electronics_2_minutes = 120, 
    printer_minutes = 240
)
api_table_manager.create_api_table()
api_table_manager.copy_api_table_to_clipboard()

# Create the Information table using the member and API tables. Information table is the one which shows the information about the members and their access rights. so that the users can check their rights.
information_table_manager = table_module.InformationTable(
    member_table_rows = member_table_manager.get_member_table_rows(),
    api_table_rows= api_table_manager.get_api_table_rows()
)
information_table_manager.create_information_table()
information_table_manager.copy_information_table_to_clipboard() # Copy the Information table to the clipboard, then paste it to the Information table in the Excell file.

# Create Sumamry PDF ========================================================================================================
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8') # Date format in Turkish

add_timestamp_to_output_pdf = True
output_pdf_name = f"groundlab_genel_rapor_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf" if add_timestamp_to_output_pdf else f"groundlab_genel_rapor.pdf"
templates_folder_path = Path(__file__).parent.resolve() / 'src' / 'templates'
pdf_output_folder_path = Path(__file__).parent.resolve() / 'pdf_files' / output_pdf_name

# Cover Page
cover_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'cover_page.pdf')
today_date = datetime.datetime.now().strftime("%d %B %Y")
cover_page.add_text(x = 88, y = 370, text = today_date, text_color=(0.54, 0.09, 0.19), size=16)

main_pdf = pdf_module.PDF()
main_pdf.add_page(cover_page)

# GL info page
gl_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'GL_info_page.pdf')
main_pdf.add_page(gl_info_page)

# Yonetim info page
yonetim_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'yonetim_info_page.pdf')
main_pdf.add_page(yonetim_info_page)

# nasıl_uye_olunur info page
nasıl_uye_olunur_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'nasıl_uye_olurum_page.pdf')
main_pdf.add_page(nasıl_uye_olunur_info_page)

# Kullanım Kuralları info page
kullanim_kurallari_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'gl_kuralları_page.pdf')
main_pdf.add_page(kullanim_kurallari_info_page)

# Kart sistemi nasıl çalışır info page
kart_sistemi_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'kart_sistemi_nasıl_calisir_page.pdf')
main_pdf.add_page(kart_sistemi_info_page)

# Elektrik ekipmanları info page
elektrik_ekipmanlari_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'elektronik_ekipman_listesi_page.pdf')
main_pdf.add_page(elektrik_ekipmanlari_info_page)

# El aletleri info page
el_aletleri_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'el_aletleri_page.pdf')
main_pdf.add_page(el_aletleri_info_page)

# Sarf Malzemeler info page
sarf_malzemeler_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'sarf_malzemesi_page.pdf')
main_pdf.add_page(sarf_malzemeler_info_page)

# Kendi atölyeni yap info page
kendi_atolyeni_yap_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'kendi_atolyeniz_page.pdf')
main_pdf.add_page(kendi_atolyeni_yap_info_page)

# Authorizations Information Table Pages
member_authorizations_info_page = pdf_module.Page(template_pdf_path= templates_folder_path / 'member_authorizations_info_page.pdf')
main_pdf.add_page(member_authorizations_info_page)

member_authorizations_list_page_template_path = templates_folder_path / 'member_authorizations_list_page.pdf'

information_table_rows = information_table_manager.get_information_table_rows()
member_per_page = 44
for i in range(0, len(information_table_rows), member_per_page):
    batch_rows = information_table_rows[i:i + member_per_page]
    if len(batch_rows) == 0:
        break
    
    new_page = pdf_module.Page(template_pdf_path= member_authorizations_list_page_template_path)
    for row_no, bath_row in enumerate(batch_rows):
        #name, is_banned_info, student_id, is_card_registered, tanitim, mechanics, electronic, printer
        new_page.add_text(x = 25, y = 696-row_no*14.95, text = str(bath_row['student_id']), size=8)
        new_page.add_text(x = 80, y = 696-row_no*14.95, text = bath_row['name'], size=8)
        new_page.add_text(x = 150, y = 696-row_no*14.95, text = bath_row['is_banned_info'], size=8)
        new_page.add_text(x = 215, y = 696-row_no*14.95, text = bath_row['is_card_registered'], size=8)
        new_page.add_text(x = 310, y = 696-row_no*14.95, text = bath_row['tanitim'], size=8)
        new_page.add_text(x = 380, y = 696-row_no*14.95, text = bath_row['electronic'], size=8)
        new_page.add_text(x = 445, y = 696-row_no*14.95, text = bath_row['printer'], size=8)
        new_page.add_text(x = 510, y = 696-row_no*14.95, text = bath_row['mechanics'], size=8)
    main_pdf.add_page(new_page)



main_pdf.save(output_pdf_path = pdf_output_folder_path)

