# 1. LOGGING MODULI - Xatoliklarni qayd qilish uchun
import logging  # Botning ishlashi davomida yuz beradigan hodisalarni (xatolar, ma'lumotlar) faylga yoki konsolga yozish uchun

# 2. QRCODE MODULI - QR kod yaratish uchun
import qrcode  # Matn yoki linkdan QR kod (tezkor javob kodi) rasmiga aylantirish uchun

# 3. ASYNCIO MODULI - Asinxron dasturlash uchun
import asyncio  # Botning bir vaqtning o'zida bir nechta foydalanuvchiga xizmat ko'rsatishini ta'minlaydi

# 4. OS MODULI - Operatsion tizim bilan ishlash uchun
import os  # Fayllarni yaratish, o'chirish va boshqa tizim amallari uchun

# 5. AIOGRAM MODULI - Telegram bot yaratish uchun asosiy kutubxona
from aiogram import Bot, Dispatcher, types  # Bot - bot obyekti, Dispatcher - xabarlarni boshqaruvchi, types - Telegram xabarlar turlari

# 6. AIOGRAM FILTERS - Xabarlarni filtrlash uchun
from aiogram.filters import Command  # /start, /help kabi buyruqlarni aniqlash uchun filter

# 7. AIOGRAM TYPES - Fayl jo'natish uchun
from aiogram.types import FSInputFile  # Lokal faylni Telegramga jo'natish uchun maxsus klass

# 8. API TOKEN - Botning maxsus kaliti
API_TOKEN = '8577685040:AAHhEi0vAV8_GXSu830GaFp5JDLBSWE_gn0'  # Botfather dan olingan bot tokeni

# 9. LOGGING SOZLAMALARI - Xatoliklarni qayd etish darajasi
logging.basicConfig(level=logging.INFO)  # INFO darajadagi va undan yuqori (WARNING, ERROR) xabarlarni konsolga chiqarish

# 10. BOT OBYEKTI - Botni ishga tushirish
bot = Bot(token=API_TOKEN)  # Berilgan token bilan bot obyektini yaratish

# 11. DISPATCHER OBYEKTI - Xabarlarni qabul qilish va tarqatish
dp = Dispatcher()  # Barcha kelgan xabarlarni tegishli handlerlarga yo'naltiruvchi obyekt

# 12. START BUYRUG'I HANDLERI - /start buyrug'iga javob
@dp.message(Command('start'))  # Dekorator - bu funksiya faqat /start buyrug'iga ishlaydi
async def send_welcome(message: types.Message):  # Asinxron funksiya (bir vaqtda ko'p so'rovga javob beradi)
    await message.reply(  # Foydalanuvchiga javob yuborish
        "👋 Salom! Menga matn yoki link yuboring, men QR kod yaratib beraman.\n\n"
        "👋 Привет! Отправьте мне текст или ссылку, и я создам QR-код!\n\n"
        "📝 Matn/Текст yuboring:"  # Ko'p tilli salomlashish xabari
    )

# 13. HELP BUYRUG'I HANDLERI - /help buyrug'iga javob
@dp.message(Command('help'))  # Bu funksiya faqat /help buyrug'iga ishlaydi
async def send_help(message: types.Message):
    await message.reply(  # Yordam xabarini yuborish
        "🤖 Botdan foydalanish:\n"
        "• Istalgan matn yoki linkni yuboring\n"
        "• Bot avtomatik QR kod yaratadi\n"
        "• QR kodni rasm sifatida yuboradi\n\n"
        "🤖 Использование:\n"
        "• Отправьте любой текст или ссылку\n"
        "• Бот автоматически создаст QR-код\n"
        "• Отправит QR-код в виде изображения"
    )

# 14. ASOSIY HANDLER - Barcha matnli xabarlar uchun
@dp.message()  # Dekoratorsiz - har qanday matnli xabarga ishlaydi
async def generate_qr_code(message: types.Message):
    data = message.text.strip()  # Foydalanuvchi yuborgan matnni olib, bo'sh joylarni tozalash
    
    # 15. MATN TEKSHIRISH - Agar matn bo'sh bo'lsa
    if not data:
        await message.reply("❌ Iltimos, matn yoki link yuboring / Пожалуйста, отправьте текст или ссылку")
        return  # Funksiyani to'xtatish
    
    # 16. JARAYON XABARI - QR kod tayyorlanayotganini bildirish
    status_msg = await message.reply("⏳ QR kod yaratilmoqda... / Создаю QR-код...")
    
    # 17. TRY-EXCEPT BLOKI - Xatoliklarni ushlash uchun
    try:
        # 18. QR KOD OBYEKTINI YARATISH
        qr = qrcode.QRCode(
            version=1,  # QR kod versiyasi (1=21x21 nuqta, katta ma'lumot uchun kattaroq versiya)
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Xatolarni tuzatish darajasi (L=7% ma'lumot tiklay oladi)
            box_size=10,  # Har bir nuqtaning pikseldagi o'lchami (10px)
            border=4,  # QR kod atrofidagi chegara (4 nuqta)
        )
        
        # 19. MA'LUMOTNI QO'SHISH
        qr.add_data(data)  # Foydalanuvchi matnini QR kodga qo'shish
        qr.make(fit=True)  # Ma'lumotga mos keladigan o'lchamni avtomatik tanlash
        
        # 20. RASM YARATISH
        img = qr.make_image(fill_color="black", back_color="white")  # Qora QR kod, oq fon
        
        # 21. FAYLNING NOMI
        filename = f"qrcode_{message.from_user.id}.png"  # Foydalanuvchi ID si bilan unikal nom (masalan: qrcode_123456789.png)
        
        # 22. RASMNI SAQLASH
        img.save(filename)  # Yaratilgan QR kodni PNG formatida diskka saqlash
        
        # 23. STATUS XABARINI O'CHIRISH
        try:
            await status_msg.delete()  # "Yaratilmoqda..." xabarini o'chirish
        except:
            pass  # Agar xabar allaqachon o'chirilgan bo'lsa, xatolikni e'tiborsiz qoldirish
        
        # 24. FAYLNI JO'NATISHGA TAYYORLASH
        photo = FSInputFile(filename)  # Lokal faylni Telegram jo'nata oladigan formatga o'tkazish
        
        # 25. QR KOD RASMINI YUBORISH
        await bot.send_photo(
            message.chat.id,  # Qaysi chatga yuborish (foydalanuvchi yoki guruh)
            photo,  # QR kod rasmi
            caption=f"✅ QR код тайёр / готов!\n\n📝 {data[:50]}{'...' if len(data) > 50 else ''}"  # Rasm ostidagi matn (50 belgidan oshsa qisqartiriladi)
        )
        
        # 26. LOYIHALIK FAYLNI O'CHIRISH
        os.remove(filename)  # Endi kerak bo'lmagan vaqtinchalik faylni diskdan o'chirish
        
    # 27. XATOLIKNI QAYD QILISH
    except Exception as e:  # Har qanday xatolik yuz bersa
        logging.error(f"Xatolik / Ошибка: {e}")  # Xatolikni log fayliga yozish
        await message.reply("❌ Xatolik yuz berdi / Произошла ошибка. Iltimos qaytadan urinib ko'ring / Пожалуйста, попробуйте снова.")  # Foydalanuvchiga xatolik haqida xabar

# 28. ASOSIY ASINXRON FUNKSIYA
async def main():
    """Botni ishga tushirish"""
    print("🤖 QR kod bot ishga tushdi...")  # Konsolga chiqarish
    print("📱 Bot Telegramda ishlayapti")
    print("💡 Botdan foydalanish: matn yoki link yuboring")
    
    # 29. BOTNI ISHGA TUSHIRISH
    await dp.start_polling(bot)  # Botni doimiy ishlash rejimiga o'tkazish (yangi xabarlarni so'rov qilib turish)

# 30. DASTURNI ISHGA TUSHIRISH
if __name__ == '__main__':  # Agar bu fayl to'g'ridan-to'g'ri ishga tushirilgan bo'lsa (import qilinmagan bo'lsa)
    asyncio.run(main())  # Asinxron main() funksiyasini ishga tushirish