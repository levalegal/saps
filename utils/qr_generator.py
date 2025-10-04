import qrcode
from io import BytesIO
from PIL import Image
from database.models import Employee

class QRGenerator:
    @staticmethod
    def generate_vcard(employee: Employee) -> str:
        vcard = f"BEGIN:VCARD\n"
        vcard += f"VERSION:3.0\n"
        vcard += f"FN:{employee.last_name} {employee.first_name}"
        if employee.middle_name:
            vcard += f" {employee.middle_name}"
        vcard += f"\n"
        vcard += f"N:{employee.last_name};{employee.first_name}"
        if employee.middle_name:
            vcard += f";{employee.middle_name}"
        vcard += f";;\n"
        
        if employee.position:
            vcard += f"TITLE:{employee.position}\n"
        
        if employee.work_phone:
            vcard += f"TEL;TYPE=WORK:{employee.work_phone}\n"
        
        if employee.mobile_phone:
            vcard += f"TEL;TYPE=CELL:{employee.mobile_phone}\n"
        
        if employee.email:
            vcard += f"EMAIL:{employee.email}\n"
        
        vcard += f"END:VCARD"
        
        return vcard
    
    @staticmethod
    def generate_qr_code(employee: Employee) -> bytes:
        vcard_data = QRGenerator.generate_vcard(employee)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(vcard_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()



