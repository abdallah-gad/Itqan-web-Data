import qrcode
from PIL import Image
import os
import re

# 1. إعداد مجلد الحفظ
output_folder = "Links_QR_Codes_login"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. قائمة اللينكات
links_data = [
    # --- لينك الدخول المدير (Manager) ---
    {"type": "مدير_الفرع", "branch": "المحلة", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=المحلة"},
    {"type": "مدير_الفرع", "branch": "المنصورة", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=المنصورة"},
    {"type": "مدير_الفرع", "branch": "طنطا", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=طنطا"},
    {"type": "مدير_الفرع", "branch": "كفر الشيخ", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=كفر%20الشيخ"},
    {"type": "مدير_الفرع", "branch": "دمنهور", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=دمنهور"},
    {"type": "مدير_الفرع", "branch": "جليم", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=جليم"},
    {"type": "مدير_الفرع", "branch": "العجمي", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=العجمي"},
    {"type": "مدير_الفرع", "branch": "دمياط الجديده", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=دمياط%20الجديده"},
    {"type": "مدير_الفرع", "branch": "شبين الكوم", "url": "https://abdallah-gad.github.io/Itqan-web-Data/manager.html?branch=شبين%20الكوم"},

    # --- لينك الدخول مشرف التكنشن (Tech Supervisor) ---
    {"type": "مشرف_التكنشن", "branch": "المحلة", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=المحلة"},
    {"type": "مشرف_التكنشن", "branch": "المنصورة", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=المنصورة"},
    {"type": "مشرف_التكنشن", "branch": "طنطا", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=طنطا"},
    {"type": "مشرف_التكنشن", "branch": "كفر الشيخ", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=كفر%20الشيخ"},
    {"type": "مشرف_التكنشن", "branch": "دمنهور", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=دمنهور"},
    {"type": "مشرف_التكنشن", "branch": "جليم", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=جليم"},
    {"type": "مشرف_التكنشن", "branch": "العجمي", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=العجمي"},
    {"type": "مشرف_التكنشن", "branch": "دمياط الجديده", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=دمياط%20الجديده"},
    {"type": "مشرف_التكنشن", "branch": "شبين الكوم", "url": "https://abdallah-gad.github.io/Itqan-web-Data/tech-supervisor.html?tech=شبين%20الكوم"},

    # --- لينك الدخول مشرف المشرفين (Supervisor) ---
    {"type": "مشرف_الفروع", "branch": "sup4", "url": "https://abdallah-gad.github.io/Itqan-web-Data/supervisor.html?sup=sup4"},
    {"type": "مشرف_الفروع", "branch": "sup5", "url": "https://abdallah-gad.github.io/Itqan-web-Data/supervisor.html?sup=sup5"},
    {"type": "مشرف_الفروع", "branch": "sup1", "url": "https://abdallah-gad.github.io/Itqan-web-Data/supervisor.html?sup=sup1"},
    {"type": "مشرف_الفروع", "branch": "sup2", "url": "https://abdallah-gad.github.io/Itqan-web-Data/supervisor.html?sup=sup2"},
    {"type": "مشرف_الفروع", "branch": "sup3", "url": "https://abdallah-gad.github.io/Itqan-web-Data/supervisor.html?sup=sup3"},
]

# 3. إعدادات ثابتة
logo_path = "icons/Itqan.png"  # تأكد إن المسار ده صح

# 4. تحميل الشعار
try:
    logo = Image.open(logo_path)
except FileNotFoundError:
    print(f"⚠️ تحذير: لم يتم العثور على الشعار في {logo_path}. سيتم توليد QR بدون شعار.")
    logo = None

# 5. عمل لوب لكل اللينكات
print(f"⏳ جاري توليد {len(links_data)} كود QR...")

for item in links_data:
    item_type = item['type']
    branch_name = item['branch']
    link = item['url']
    
    # توليد الكود
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # لون الكود (أسود أو أزرق غامق)
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

    # تنظيف اسم الفرع من الرموز
    safe_branch = re.sub(r'[\\/*?:"<>|]', "", branch_name).strip()
    
    # اسم الملف النهائي
    filename = f"{item_type} - {safe_branch}.png"
    filepath = os.path.join(output_folder, filename)
    
    # حفظ الصورة
    qr_img.save(filepath)
    print(f"  ✅ تم إنشاء: {filename}")

print(f"\n🎉 تم الانتهاء بنجاح! اتولدت {len(links_data)} صورة QR في فولدر '{output_folder}'.")