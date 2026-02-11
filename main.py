import telebot
from telebot import types
import os  # مكتبة للتعامل مع ملفات النظام

TOKEN = '8410868580:AAGnJDepOVMVcRCYXnQ4nHshT2Q_bQUYPdY'
bot = telebot.TeleBot(TOKEN)

# مجلد الملفات (تأكد من إنشاء مجلد بهذا الاسم في PythonAnywhere ورفع ملفاتك داخله)
FILES_FOLDER = 'my_files/'

user_status = {}

@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'الرجوع إلى البداية')
def main_menu(message):
    user_status[message.chat.id] = None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('المستوى الثاني 2️⃣'), types.KeyboardButton('المستوى الاول 1️⃣'))
    markup.row(types.KeyboardButton('المستوى الرابع 4️⃣'), types.KeyboardButton('المستوى الثالث 3️⃣'))
    markup.add('📖 معلومات عامة عن الأمن السيبراني', 'قنوات تعليمية للمقررات')
    bot.send_message(message.chat.id, "مرحباً بك.. اختر المستوى:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['المستوى الاول 1️⃣', 'المستوى الثاني 2️⃣'])
def choose_term(message):
    user_status[message.chat.id] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('الترم الاول'), types.KeyboardButton('الترم الثاني'))
    markup.add('الرجوع إلى البداية')
    bot.send_message(message.chat.id, f"اختر الترم لـ {message.text}:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['الترم الاول', 'الترم الثاني'])
def list_subjects(message):
    level = user_status.get(message.chat.id)
    term = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if level == 'المستوى الاول 1️⃣' and term == 'الترم الاول':
        markup.add('مبادئ البرمجة', 'مهارات الاتصال', 'اللغة العربية 1', 'أساسيات الحوسبة', 'رياضيات 1', 'اللغة الإنجليزية 1')
    elif level == 'المستوى الاول 1️⃣' and term == 'الترم الثاني':
        markup.add('اللغه العربيه 11', 'الثقافه الاسلاميه', 'رياضيات 11', 'رياضيات متقطعة', 'أساسيات الأمن السيبراني', 'برمجة الحاسوب')
    elif level == 'المستوى الثاني 2️⃣' and term == 'الترم الاول':
        markup.add('انجليزي تقني', 'أساسيات قواعد البيانات', 'هياكل البيانات والخوارزميات', 'تصميم المنطق الرقمي', 'تحليل وتصميم النظم', 'الإحصاء والاحتمالات')
    elif level == 'المستوى الثاني 2️⃣' and term == 'الترم الثاني':
        markup.add('تراسل البيانات و الشبكات', 'البرمجة الموجهة بالكائنات', 'معمارية وتنظيم الحاسب', 'اساسيات تصميم الويب', 'علم التشفير', 'القانون والخصوصية')

    markup.add('الرجوع إلى البداية')
    bot.send_message(message.chat.id, "اختر المادة لتحميل الملف:", reply_markup=markup)

# --- الدالة الذكية لإرسال أي ملف بأي امتداد ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    subject_name = message.text
    found = False

    # التأكد من وجود المجلد
    if not os.path.exists(FILES_FOLDER):
        os.makedirs(FILES_FOLDER)

    # البحث عن أي ملف يبدأ باسم المادة داخل المجلد
    for file in os.listdir(FILES_FOLDER):
        # سنقوم بمطابقة اسم الملف مع اسم الزر (بدون الامتداد)
        file_name_without_ext = os.path.splitext(file)[0]
        
        if file_name_without_ext == subject_name:
            file_path = os.path.join(FILES_FOLDER, file)
            with open(file_path, 'rb') as doc:
                bot.send_document(message.chat.id, doc, caption=f"إليك ملف مادة: {subject_name}")
            found = True
            break
    
    if not found and subject_name not in ['الترم الاول', 'الترم الثاني', 'الرجوع إلى البداية']:
        bot.reply_to(message, "سيتم رفع ملفات هذه المادة قريباً.. ⏳")

bot.polling()
