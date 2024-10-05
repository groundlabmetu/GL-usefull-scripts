from pathlib import Path
from modules import pdf_module, table_module


csv_folder_path = Path(__file__).parent.resolve() / 'csv_files'
member_table_path = csv_folder_path / 'Ground Lab Üyeler - Aktif üyeler.csv'
card_requests_table_path = csv_folder_path / 'Masa kullanımı ile ilgili request (Yanıtlar) - Form Yanıtları 1.csv'

member_table_manager = table_module.MemberTable(member_table_path)
member_table_manager.validate_member_table()

card_requests_table_manager = table_module.CardRequestsTable(card_requests_table_path)

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

information_table_manager = table_module.InformationTable(
    member_table_rows = member_table_manager.get_member_table_rows(),
    api_table_rows= api_table_manager.get_api_table_rows()
)
information_table_manager.create_information_table()
information_table_manager.copy_information_table_to_clipboard()