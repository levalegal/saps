from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from database.models import Employee

class CardGenerator:
    @staticmethod
    def generate_business_card(employee: Employee, include_qr: bool = False) -> bytes:
        width = 600
        height = 350
        
        card = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(card)
        
        try:
            title_font = ImageFont.truetype('arial.ttf', 28)
            normal_font = ImageFont.truetype('arial.ttf', 18)
            small_font = ImageFont.truetype('arial.ttf', 14)
        except:
            title_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        draw.rectangle([(0, 0), (width, 80)], fill='#2c3e50')
        
        full_name = f"{employee.last_name} {employee.first_name}"
        if employee.middle_name:
            full_name += f" {employee.middle_name}"
        
        draw.text((20, 25), full_name, fill='white', font=title_font)
        
        y_position = 100
        
        if employee.position:
            draw.text((20, y_position), f"Должность: {employee.position}", fill='#2c3e50', font=normal_font)
            y_position += 35
        
        if employee.work_phone:
            draw.text((20, y_position), f"Телефон: {employee.work_phone}", fill='#34495e', font=normal_font)
            y_position += 30
        
        if employee.mobile_phone:
            draw.text((20, y_position), f"Мобильный: {employee.mobile_phone}", fill='#34495e', font=normal_font)
            y_position += 30
        
        if employee.email:
            draw.text((20, y_position), f"Email: {employee.email}", fill='#34495e', font=normal_font)
            y_position += 30
        
        if employee.telegram:
            draw.text((20, y_position), f"Telegram: {employee.telegram}", fill='#3498db', font=small_font)
            y_position += 25
        
        if employee.whatsapp:
            draw.text((20, y_position), f"WhatsApp: {employee.whatsapp}", fill='#25d366', font=small_font)
            y_position += 25
        
        if employee.skype:
            draw.text((20, y_position), f"Skype: {employee.skype}", fill='#00aff0', font=small_font)
        
        if include_qr and employee.email:
            try:
                from utils.qr_generator import QRGenerator
                qr_data = QRGenerator.generate_qr_code(employee)
                qr_image = Image.open(BytesIO(qr_data))
                qr_image = qr_image.resize((150, 150))
                card.paste(qr_image, (430, 100))
            except:
                pass
        
        buffer = BytesIO()
        card.save(buffer, format='PNG')
        return buffer.getvalue()
    
    @staticmethod
    def generate_contact_sheet(employees: list, title: str = "Сотрудники") -> bytes:
        card_width = 280
        card_height = 200
        cards_per_row = 3
        padding = 20
        
        rows = (len(employees) + cards_per_row - 1) // cards_per_row
        width = cards_per_row * card_width + (cards_per_row + 1) * padding
        height = rows * card_height + (rows + 1) * padding + 60
        
        sheet = Image.new('RGB', (width, height), color='#ecf0f1')
        draw = ImageDraw.Draw(sheet)
        
        try:
            title_font = ImageFont.truetype('arial.ttf', 32)
            name_font = ImageFont.truetype('arial.ttf', 16)
            small_font = ImageFont.truetype('arial.ttf', 12)
        except:
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        draw.text((width // 2 - 100, 15), title, fill='#2c3e50', font=title_font)
        
        for idx, employee in enumerate(employees):
            row = idx // cards_per_row
            col = idx % cards_per_row
            
            x = col * card_width + (col + 1) * padding
            y = row * card_height + (row + 1) * padding + 60
            
            draw.rectangle([(x, y), (x + card_width, y + card_height)], 
                         fill='white', outline='#bdc3c7', width=2)
            
            full_name = f"{employee.last_name} {employee.first_name}"
            if employee.middle_name:
                full_name = f"{employee.last_name} {employee.first_name[0]}. {employee.middle_name[0]}."
            
            draw.text((x + 10, y + 10), full_name, fill='#2c3e50', font=name_font)
            
            text_y = y + 40
            if employee.position:
                draw.text((x + 10, text_y), employee.position[:30], fill='#7f8c8d', font=small_font)
                text_y += 25
            
            if employee.work_phone:
                draw.text((x + 10, text_y), f"☎ {employee.work_phone}", fill='#34495e', font=small_font)
                text_y += 25
            
            if employee.email:
                email_text = employee.email[:28]
                draw.text((x + 10, text_y), f"✉ {email_text}", fill='#34495e', font=small_font)
                text_y += 25
            
            if employee.telegram:
                draw.text((x + 10, text_y), f"TG: {employee.telegram}", fill='#0088cc', font=small_font)
        
        buffer = BytesIO()
        sheet.save(buffer, format='PNG')
        return buffer.getvalue()




