# 1. REQUESTS MODULI - HTTP so'rovlar yuborish uchun
import requests  # Internet orqali API ga so'rov yuborish va javob olish uchun (cbu.uz dan valyuta kurslarini olish)

# 2. ASYNCIO MODULI - Asinxron dasturlash uchun
import asyncio  # Botning bir vaqtning o'zida ko'p foydalanuvchilarga xizmat ko'rsatishi uchun

# 3. LOGGING MODULI - Xatoliklarni qayd qilish uchun
import logging  # Botning ishlashi davomida yuz beradigan hodisalarni (xatolar, ma'lumotlar) konsolga yozish uchun

# 4. AIOGRAM MODULI - Telegram bot yaratish uchun asosiy kutubxona
from aiogram import Bot, Dispatcher, types  # Bot - bot obyekti, Dispatcher - xabarlarni boshqaruvchi, types - Telegram xabarlar turlari

# 5. AIOGRAM FILTERS - Xabarlarni filtrlash uchun
from aiogram.filters import Command  # /start, /help kabi buyruqlarni aniqlash uchun filter

# 6. AIOGRAM ENUMS - Matn formatlash uchun
from aiogram.enums import ParseMode  # Matnni HTML yoki Markdown formatda yuborish imkoniyati (hozir ishlatilmagan)

# 7. API TOKEN - Botning maxsus kaliti
API_TOKEN = "8577685040:AAHhEi0vAV8_GXSu830GaFp5JDLBSWE_gn0"  # Botfather dan olingan bot tokeni

# 8. LOGGING SOZLAMALARI
logging.basicConfig(level=logging.INFO)  # INFO darajadagi va undan yuqori xabarlarni konsolga chiqarish

# 9. BOT OBYEKTI
bot = Bot(token=API_TOKEN)  # Berilgan token bilan bot obyektini yaratish

# 10. DISPATCHER OBYEKTI
dp = Dispatcher()  # Barcha kelgan xabarlarni handlerlarga yo'naltiruvchi obyekt

# 11. VALYUTALAR LUG'ATI - Mavjud valyutalar ro'yxati
CURRENCIES = {  # Kalit - valyuta kodi, Qiymat - valyuta nomi
    'USD': 'AQSH dollari',      # Amerika Qo'shma Shtatlari dollari
    'EUR': 'Yevro',              # Yevropa Ittifoqi valyutasi
    'RUB': 'Rossiya rubli',      # Rossiya rubli
    'GBP': 'Angliya funti',      # Buyuk Britaniya funti
    'JPY': 'Yapon iyenasi',      # Yaponiya iyenasi
    'CNY': 'Xitoy yuani',        # Xitoy yuani
    'KRW': 'Janubiy Koreya voni', # Janubiy Koreya voni
    'TRY': 'Turk lirasi',        # Turk lirasi
    'KZT': "Qozog'iston tengesi", # Qozog'iston tengesi
    'UZS': "O'zbekiston so'mi"   # O'zbekiston so'mi (asosiy valyuta)
}

# 12. START BUYRUG'I HANDLERI
@dp.message(Command('start'))  # /start buyrug'iga javob beruvchi dekorator
async def send_welcome(message: types.Message):  # Asinxron funksiya
    welcome_text = """  # Ko'p qatorli matn (salomlashish va ko'rsatma)
💱 Valyuta kurslari botiga xush kelibsiz!

📝 Mavjud valyutalar:
• USD - AQSH dollari
• EUR - Yevro
• RUB - Rossiya rubli
# ... (qolgan valyutalar)
"""
    await message.reply(welcome_text)  # Foydalanuvchiga xabarni qaytarish

# 13. HELP BUYRUG'I HANDLERI
@dp.message(Command('help'))  # /help buyrug'iga javob
async def send_help(message: types.Message):
    help_text = """  # Yordam matni
🤖 Botdan foydalanish:

1️⃣ Valyuta kodini yuboring (USD, EUR, RUB, GBP, JPY)
2️⃣ Bot sizga joriy kursni yuboradi
# ... (qolgan ko'rsatmalar)
"""
    await message.reply(help_text)  # Yordam xabarini yuborish

# 14. VALYUTALAR RO'YXATI BUYRUG'I
@dp.message(Command('currencies'))  # /currencies buyrug'iga javob
async def list_currencies(message: types.Message):
    text = "📋 Mavjud valyutalar / Доступные валюты:\n\n"  # Sarlavha
    for code, name in CURRENCIES.items():  # Lug'atdagi barcha valyutalarni aylanish
        text += f"• {code} - {name}\n"  # Har bir valyutani qo'shish
    await message.reply(text)  # Ro'yxatni yuborish

# 15. ASOSIY HANDLER - Foydalanuvchi xabarlari uchun
@dp.message()  # Hech qanday filter yo'q - barcha matnli xabarlar shu yerga keladi
async def handle_message(message: types.Message):
    code = message.text.strip().upper()  # Foydalanuvchi matnini olib, bo'sh joylarni tozalash va katta harflarga o'tkazish
    
    # 16. VALYUTA KODINI TEKSHIRISH
    if len(code) > 10:  # Agar kod 10 belgidan uzun bo'lsa (noto'g'ri format)
        await message.reply("❌ Noto'g'ri format / Неверный формат. Valyuta kodini yuboring (USD, EUR, RUB...)")
        return  # Funksiyani to'xtatish
    
    # 17. STATUS XABARI - Qidirilayotganini bildirish
    status_msg = await message.reply(f"⏳ {code} kursi qidirilmoqda... / Ищу курс {code}...")
    
    # 18. TRY-EXCEPT BLOKI - Xatoliklarni ushlash
    try:
        # 19. API SO'ROVI - CBU serveriga so'rov yuborish
        response = requests.get(
            "https://cbu.uz/uz/arkhiv-kursov-valyut/json/",  # API manzili (Markaziy bank valyuta kurslari)
            timeout=10  # 10 soniyada javob kelmasa, timeout xatosi
        )
        response.raise_for_status()  # Agar status kod 200 bo'lmasa (masalan 404, 500), exception tashlaydi
        
        # 20. MA'LUMOTNI QAYTA ISHLASH
        data = response.json()  # JSON formatdagi javobni Python lug'atiga o'tkazish
        found = None  # Topilgan valyutani saqlash uchun o'zgaruvchi
        
        # 21. VALYUTANI QIDIRISH - API dan kelgan ma'lumotlarni aylanish
        for item in data:  # Har bir valyuta obyekti uchun
            if item.get('Ccy') == code:  # Agar valyuta kodi mos kelsa
                found = item  # Topilgan valyutani saqlash
                break  # Qidiruvni to'xtatish (topdik)
        
        # 22. STATUS XABARINI O'CHIRISH
        try:
            await status_msg.delete()  # "Qidirilmoqda..." xabarini o'chirish
        except:
            pass  # Agar xabar allaqachon o'chirilgan bo'lsa, xatolikni e'tiborsiz qoldirish
        
        # 23. AGAR VALYUTA TOPILMASA
        if not found:
            # Eng yaqin valyutalarni taklif qilish
            suggestions = [c for c in CURRENCIES.keys() if code in c]  # Kod qisman mos keladigan valyutalar
            if suggestions:  # Agar takliflar mavjud bo'lsa
                suggest_text = f"❌ {code} topilmadi / не найдена.\n\n📝 Taklif / Предложение: {', '.join(suggestions[:3])}\n\n📋 Barcha valyutalar: /currencies"
            else:  # Hech qanday taklif bo'lmasa
                suggest_text = f"❌ {code} topilmadi / не найдена.\n\n📋 Mavjud valyutalar / Доступные валюты:\n" + \
                              ", ".join(list(CURRENCIES.keys())[:10]) + "...\n\n💡 /currencies - barcha valyutalar"
            
            await message.reply(suggest_text)  # Taklif xabarini yuborish
            return  # Funksiyani to'xtatish
        
        # 24. MA'LUMOTLARNI AYRISH - Topilgan valyutaning ma'lumotlari
        currency_name = found.get('CcyNm_UZ', found.get('CcyNm_RU', code))  # Valyuta nomi (uzbekcha, agar bo'lmasa ruscha, bo'lmasa kod)
        rate = found.get('Rate', '0')  # Valyuta kursi (1 birlik valyuta necha so'm)
        date = found.get('Date', 'N/A')  # Kurs amal qiladigan sana
        
        # 25. JAVOB MATNINI FORMATLASH
        text = f"""
💱 {currency_name} ({code})

💰 Kurs / Курс: 
• 1 {code} = {rate} so'm

📅 Sana / Дата: {date}

📊 Ma'lumot manbai: cbu.uz
"""
        await message.reply(text)  # Kurs ma'lumotlarini yuborish
        
        # 26. LOG QILISH - Konsolga ma'lumot chiqarish
        print(f"✅ {message.from_user.id} - {code}: {rate} so'm")  # Foydalanuvchi ID si, valyuta kodi va kurs
        
    # 27. XATOLIKLARNI USHLASH - TURLI XATOLIK TURLARI
    except requests.exceptions.Timeout:  # Agar server 10 soniyada javob bermasa
        await message.reply("⏰ Server bilan bog'lanishda vaqt tugadi / Таймаут подключения к серверу.\nIltimos qaytadan urinib ko'ring.")
    
    except requests.exceptions.ConnectionError:  # Agar internet aloqasi bo'lmasa
        await message.reply("🌐 Internet aloqasi yo'q / Нет интернет соединения.\nIltimos aloqani tekshiring.")
    
    except requests.exceptions.RequestException as e:  # Boshqa HTTP bilan bog'liq xatolar
        print(f"Request error: {e}")  # Xatolikni konsolga chiqarish
        await message.reply("❌ Ma'lumot olishda xatolik / Ошибка получения данных.\nIltimos qaytadan urinib ko'ring.")
    
    except Exception as e:  # Kutilmagan boshqa xatolar
        print(f"Unexpected error: {e}")  # Xatolikni konsolga chiqarish
        await message.reply("❌ Kutilmagan xatolik / Неожиданная ошибка.\nIltimos qaytadan urinib ko'ring.")

# 28. ASOSIY FUNKSIYA - Botni ishga tushirish
async def main():
    """Botni ishga tushirish"""
    print("=" * 40)  # Chiroyli ajratuvchi chiziq
    print("💱 Valyuta kurslari boti ishga tushdi...")
    print("📱 Bot Telegramda ishlayapti")
    print("📊 Valyuta kurslari cbu.uz dan olinadi")
    print("💡 Misol: USD, EUR, RUB yuboring")
    print("=" * 40)
    
    # 29. BOTNI POLLING REJIMIDA ISHLATISH
    await dp.start_polling(bot)  # Botni doimiy ishlash rejimiga o'tkazish (yangi xabarlarni so'rov qilib turish)

# 30. DASTURNI ISHGA TUSHIRISH
if __name__ == "__main__":  # Agar bu fayl to'g'ridan-to'g'ri ishga tushirilgan bo'lsa
    try:
        asyncio.run(main())  # Asinxron main() funksiyasini ishga tushirish
    except KeyboardInterrupt:  # Agar foydalanuvchi Ctrl+C bossa
        print("\n❌ Bot to'xtatildi / Бот остановлен")  # Xabarni chiqarish va to'xtatish