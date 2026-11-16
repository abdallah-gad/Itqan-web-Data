import qrcode
from PIL import Image
import os
import re

# 1. إعداد مجلد الحفظ
output_folder = "QR_Codes"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. قراءة ملف data.js واستخراج البيانات بـ Regex
try:
    with open("data.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    # استخراج كل الأجهزة باستخدام regex
    # بندور على id: رقم، وبعده name: "نص"
    pattern = re.compile(r'id:\s*(\d+),\s*name:\s*"([^"]+)"')
    matches = pattern.findall(content)
    
    devices = []
    for match in matches:
        devices.append({
            'id': int(match[0]),
            'name': match[1]
        })
        
    if not devices:
        print("❌ لم يتم العثور على أجهزة في ملف data.js. تأكد من صيغة الملف.")
        exit()
        
except FileNotFoundError:
    print("❌ خطأ: لم يتم العثور على ملف data.js. تأكد من وجوده في نفس المجلد.")
    exit()
except Exception as e:
    print(f"❌ خطأ في قراءة البيانات: {e}")
    exit()

# 3. إعدادات ثابتة
base_url = "https://abdallah-gad.github.io/Itqan-web-Data/device.html?id="
logo_path = "icons/Itqan.png"  # تأكد إن المسار ده صح

# 4. تحميل الشعار
try:
    logo = Image.open(logo_path)
except FileNotFoundError:
    print(f"⚠️ تحذير: لم يتم العثور على الشعار في {logo_path}. سيتم توليد QR بدون شعار.")
    logo = None

# 5. عمل لوب لكل الأجهزة
print(f"⏳ جاري توليد {len(devices)} كود QR...")

for dev in devices:
    dev_id = dev['id']
    dev_name = dev['name']
    
    # الرابط المخصص
    link = f"{base_url}{dev_id}"
    
    # توليد الكود
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="#0b3d91", back_color="white").convert('RGB')

    # دمج الشعار
    if logo:
        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * 0.25)
        
        current_logo = logo.copy().resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        if current_logo.mode in ('RGBA', 'LA') or (current_logo.mode == 'P' and 'transparency' in current_logo.info):
            qr_img.paste(current_logo, pos, mask=current_logo.convert('RGBA'))
        else:
            qr_img.paste(current_logo, pos)

    # تنظيف اسم الجهاز من الرموز
    safe_name = re.sub(r'[\\/*?:"<>|]', "", dev_name).strip()
    
    # اسم الملف
    filename = f"{dev_id}- {safe_name}.png"
    filepath = os.path.join(output_folder, filename)
    
    # حفظ الصورة
    qr_img.save(filepath)
    print(f"  ✅ تم إنشاء: {filename}")

print(f"\n🎉 تم الانتهاء بنجاح! اتولدت {len(devices)} صورة QR في فولدر '{output_folder}'.")