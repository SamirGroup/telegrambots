# 1. LOGGING MODULI - Xatoliklarni qayd qilish uchun
import logging  # Botning ishlashi davomida yuz beradigan hodisalarni faylga yoki konsolga yozish uchun

# 2. ASYNCIO MODULI - Asinxron dasturlash uchun
import asyncio  # Botning bir vaqtning o'zida bir nechta foydalanuvchiga xizmat ko'rsatishini ta'minlaydi

# 3. WIKIPEDIA MODULI - Vikipediyadan ma'lumot olish uchun
import wikipedia  # Vikipediya ma'lumotlar bazasiga ulanish va maqolalarni olish uchun kutubxona

# 4. AIOGRAM MODULI - Telegram bot yaratish uchun
from aiogram import Bot, Dispatcher, types  # Bot - bot obyekti, Dispatcher - xabarlarni boshqaruvchi, types - Telegram xabarlar turlari

# 5. AIOGRAM FILTERS - Xabarlarni filtrlash uchun
from aiogram.filters import Command  # /start, /help kabi buyruqlarni aniqlash uchun filter

# 6. LOGGING SOZLAMALARI - Xatoliklarni qayd etish formatini sozlash
logging.basicConfig(  # Log tizimini sozlash
    level=logging.INFO,  # INFO darajadagi va undan yuqori xabarlarni qayd qilish
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Vaqt, nom, daraja, xabar formatida yozish
)

# 7. API TOKEN - Botning maxsus kaliti
API_TOKEN = '8577685040:AAHhEi0vAV8_GXSu830GaFp5JDLBSWE_gn0'  # Botfather dan olingan bot tokeni

# 8. BOT OBYEKTI
bot = Bot(token=API_TOKEN)  # Berilgan token bilan bot obyektini yaratish

# 9. DISPATCHER OBYEKTI
dp = Dispatcher()  # Barcha kelgan xabarlarni tegishli handlerlarga yo'naltiruvchi obyekt

# 10. WIKIPEDIA TILINI SOZLASH - Asosiy tilni o'zbek tiliga o'rnatish
try:
    wikipedia.set_lang('uz')  # Vikipediya tilini o'zbek tiliga o'rnatish
    current_lang = wikipedia.lang()  # Hozirgi tilni olish (lang() - to'g'ri metod)
    print(f"✅ Wikipedia tili: O'zbekcha ({current_lang})")  # Konsolga tasdiq xabarini chiqarish
except Exception as e:  # Agar xatolik yuz bersa
    print(f"⚠️ Wikipedia til sozlamasida xatolik: {e}")  # Xatolikni konsolga chiqarish
    wikipedia.set_lang('ru')  # Rus tiliga o'tish (zaxira varianti)
    print(f"✅ Wikipedia tili: Ruscha")  # Konsolga tasdiq xabarini chiqarish

# 11. TILNI OLISH FUNKSIYASI
def get_current_language():
    """Hozirgi tilni olish"""
    try:
        return wikipedia.lang()  # Wikipedia'dan hozirgi tilni olish
    except:
        return 'uz'  # Xatolik bo'lsa, o'zbek tilini qaytarish

# 12. START BUYRUG'I HANDLERI
@dp.message(Command('start'))  # /start buyrug'iga javob beruvchi dekorator
async def send_welcome(message: types.Message):  # Asinxron funksiya
    welcome_text = """  # Ko'p qatorli salomlashish matni
📚 **Wikipedia botiga xush kelibsiz!**

🔍 **Qanday ishlatish:**
Menga istalgan mavzu nomini yozing, men Wikipedia'dan qisqacha ma'lumot beraman.

📝 **Misol:**
• Toshkent
• Alisher Navoiy
• Kompyuter

🌐 **Komandalar:**
/start - Boshlash
/help - Yordam
/lang - Tilni o'zgartirish

💡 **Bot haqida:**
Wikipedia ma'lumotlar bazasidan foydalanadi
"""
    await message.reply(welcome_text, parse_mode="Markdown")  # Markdown formatida yuborish (qalin, kursiv va boshqalar)

# 13. HELP BUYRUG'I HANDLERI
@dp.message(Command('help'))  # /help buyrug'iga javob
async def send_help(message: types.Message):
    help_text = """  # Yordam matni
🤖 **Yordam:**

📝 **Botdan foydalanish:**
1. Istalgan mavzu nomini yozing
2. Bot Wikipedia'dan qisqacha ma'lumot beradi
3. Ma'lumot juda uzun bo'lsa, qisqartirib yuboriladi

🌍 **Mavzular:**
• Shaharlar (Toshkent, London, Nyu-York)
• Shaxslar (Alisher Navoiy, Amir Temur)
# ... (qolgan matn)
"""
    await message.reply(help_text, parse_mode="Markdown")  # Yordam xabarini yuborish

# 14. TILNI KO'RSATISH BUYRUG'I
@dp.message(Command('lang'))  # /lang buyrug'iga javob
async def show_lang(message: types.Message):
    try:
        current_lang = wikipedia.lang()  # Hozirgi tilni olish
    except:
        current_lang = 'uz'  # Xatolik bo'lsa o'zbek tilini ishlatish
    
    # 15. TIL NOMLARI LUG'ATI
    lang_names = {  # Kodlarni to'liq nomlarga o'tkazish
        'uz': 'Oʻzbekcha',  # O'zbek tili
        'ru': 'Русский',    # Rus tili
        'en': 'English'     # Ingliz tili
    }
    lang_name = lang_names.get(current_lang, current_lang)  # Lug'atdan nomni olish, topilmasa kodni ishlatish
    
    # 16. TIL HAQIDA MA'LUMOT MATNI
    lang_text = f"""
🌐 **Hozirgi til:** {lang_name}

📝 **Tilni o'zgartirish uchun:**
/lang_uz - Oʻzbekcha
/lang_ru - Ruscha
/lang_en - Inglizcha

**Пример смены языка:**
/lang_ru
"""
    await message.reply(lang_text)  # Til ma'lumotlarini yuborish

# 17. O'ZBEK TILIGA O'TISH BUYRUG'I
@dp.message(Command('lang_uz'))  # /lang_uz buyrug'iga javob
async def set_lang_uz(message: types.Message):
    try:
        wikipedia.set_lang('uz')  # Vikipediya tilini o'zbek tiliga o'rnatish
        await message.reply("✅ Til O'zbek tiliga o'zgartirildi")  # Foydalanuvchiga xabar
        print(f"Til o'zgartirildi: uz")  # Konsolga log yozish
    except Exception as e:  # Xatolik yuz bersa
        await message.reply(f"❌ Xatolik: {e}")  # Xatolik xabarini yuborish

# 18. RUS TILIGA O'TISH BUYRUG'I
@dp.message(Command('lang_ru'))  # /lang_ru buyrug'iga javob
async def set_lang_ru(message: types.Message):
    try:
        wikipedia.set_lang('ru')  # Vikipediya tilini rus tiliga o'rnatish
        await message.reply("✅ Язык изменен на Русский")  # Foydalanuvchiga xabar
        print(f"Til o'zgartirildi: ru")  # Konsolga log yozish
    except Exception as e:  # Xatolik yuz bersa
        await message.reply(f"❌ Ошибка: {e}")  # Xatolik xabarini yuborish

# 19. INGLIZ TILIGA O'TISH BUYRUG'I
@dp.message(Command('lang_en'))  # /lang_en buyrug'iga javob
async def set_lang_en(message: types.Message):
    try:
        wikipedia.set_lang('en')  # Vikipediya tilini ingliz tiliga o'rnatish
        await message.reply("✅ Language changed to English")  # Foydalanuvchiga xabar
        print(f"Til o'zgartirildi: en")  # Konsolga log yozish
    except Exception as e:  # Xatolik yuz bersa
        await message.reply(f"❌ Error: {e}")  # Xatolik xabarini yuborish

# 20. ASOSIY HANDLER - Barcha matnli xabarlar uchun (Wikipedia qidiruvi)
@dp.message()  # Hech qanday filter yo'q - barcha matnli xabarlar shu yerga keladi
async def send_summary(message: types.Message):
    query = message.text.strip()  # Foydalanuvchi yuborgan matnni olib, bo'sh joylarni tozalash
    
    # 21. MATN TEKSHIRISH
    if not query:  # Agar matn bo'sh bo'lsa
        await message.reply("❌ Iltimos, qidiruv matnini yozing")  # Xatolik xabari
        return  # Funksiyani to'xtatish
    
    # 22. STATUS XABARI - Qidirilayotganini bildirish
    status_msg = await message.reply(f"⏳ Qidirilmoqda: **{query}**...", parse_mode="Markdown")  # "Qidirilmoqda..." xabari
    
    # 23. TRY-EXCEPT BLOKI - Turli xatoliklarni ushlash
    try:
        # 24. WIKIPEDIADAN MA'LUMOT OLISH
        article = wikipedia.page(query, auto_suggest=True)  # Maqolani qidirish (auto_suggest - avtomatik taklif)
        summary = article.summary  # Maqolaning qisqacha mazmunini olish
        
        # 25. MA'LUMOTNI QISQARTIRISH (agar juda uzun bo'lsa)
        max_length = 3500  # Maksimal belgilar soni (Telegram cheklovi 4096)
        if len(summary) > max_length:  # Agar ma'lumot maksimaldan uzun bo'lsa
            summary = summary[:max_length] + "..."  # Kesib olish va nuqta qo'yish
        
        # 26. STATUS XABARINI O'CHIRISH
        try:
            await status_msg.delete()  # "Qidirilmoqda..." xabarini o'chirish
        except:
            pass  # Agar xabar allaqachon o'chirilgan bo'lsa, xatolikni e'tiborsiz qoldirish
        
        # 27. JAVOB MATNINI TAYYORLASH
        response = f"📚 **{article.title}**\n\n{summary}\n\n🔗 [Wikipedia'da o'qish]({article.url})"  # Formatlangan javob
        
        # 28. JAVOBNI YUBORISH
        await message.reply(response, parse_mode="Markdown", disable_web_page_preview=True)  # Link prev'yuini o'chirish
        
        # 29. LOG QILISH
        print(f"✅ {message.from_user.id} - {query} -> {article.title}")  # Konsolga muvaffaqiyatli qidiruv haqida yozish
        
    # 30. DISAMBIGUATION XATOSI - Bir nechta variantlar mavjud
    except wikipedia.exceptions.DisambiguationError as e:  # Masalan: "Apple" (meva yoki kompaniya)
        try:
            await status_msg.delete()  # Status xabarini o'chirish
        except:
            pass
        
        options = e.options[:10]  # Faqat birinchi 10 variantni olish
        options_text = "\n".join([f"• {opt}" for opt in options])  # Variantlarni formatlash
        
        await message.reply(
            f"🔍 **Ko'p ma'lumot topildi!**\n\n"
            f"Quyidagilardan birini tanlang:\n\n"
            f"{options_text}\n\n"
            f"💡 Aniqroq nom yozing"
        )
    
    # 31. PAGE ERROR - Maqola topilmadi
    except wikipedia.exceptions.PageError:  # Bunday maqola mavjud emas
        try:
            await status_msg.delete()  # Status xabarini o'chirish
        except:
            pass
        
        # Hozirgi tilni olish
        try:
            current_lang = wikipedia.lang()  # Hozirgi tilni olish
        except:
            current_lang = 'uz'  # Xatolik bo'lsa o'zbek tilini ishlatish
        
        # Til nomini aniqlash
        lang_name = "O'zbek" if current_lang == 'uz' else "Rus" if current_lang == 'ru' else "Ingliz"
        
        await message.reply(
            f"❌ **'{query}' topilmadi**\n\n"
            f"🌐 Hozirgi til: {lang_name}\n\n"
            f"💡 **Maslahatlar:**\n"
            f"• To'g'ri imloni tekshiring\n"
            f"• Boshqa tilni sinab ko'ring: /lang\n"
            f"• Qisqaroq so'z yozing\n"
            f"• Lotin alifbosida yozing"
        )
    
    # 32. WIKIPEDIA EXCEPTION - Boshqa Wikipedia xatolari
    except wikipedia.exceptions.WikipediaException as e:  # Wikipedia kutubxonasining boshqa xatolari
        try:
            await status_msg.delete()  # Status xabarini o'chirish
        except:
            pass
        
        await message.reply(
            f"⚠️ **Wikipedia xatosi:**\n"
            f"{str(e)[:200]}\n\n"  # Xatolik matnini qisqartirib ko'rsatish
            f"💡 Qaytadan urinib ko'ring"
        )
    
    # 33. KUZATMAGAN XATOLIKLAR
    except Exception as e:  # Boshqa barcha kutilmagan xatolar
        logging.error(f"Xatolik: {e}")  # Xatolikni log fayliga yozish
        try:
            await status_msg.delete()  # Status xabarini o'chirishga urinish
        except:
            pass
        
        await message.reply(
            f"❌ **Kutilmagan xatolik**\n\n"
            f"💡 Qaytadan urinib ko'ring yoki /help"
        )

# 34. ASOSIY ASINXRON FUNKSIYA - Botni ishga tushirish
async def main():
    """Botni ishga tushirish"""
    print("=" * 50)  # Chiroyli ajratuvchi chiziq (50 ta teng belgi)
    print("📚 Wikipedia boti ishga tushmoqda...")
    print(f"🤖 Bot token: {API_TOKEN[:10]}...")  # Tokenni faqat birinchi 10 ta belgisini ko'rsatish (xavfsizlik)
    
    # 35. HOZIRGI TILNI OLISH VA KO'RSATISH
    try:
        current_lang = wikipedia.lang()  # Hozirgi tilni olish
        lang_name = "O'zbek" if current_lang == 'uz' else "Rus" if current_lang == 'ru' else "Ingliz"  # Til nomi
        print(f"🌐 Hozirgi til: {lang_name} ({current_lang})")  # Konsolga chiqarish
    except:
        print(f"🌐 Hozirgi til: O'zbek (uz)")  # Xatolik bo'lsa standart
    
    print("📱 Bot Telegramda ishlayapti")
    print("💡 Matn yuboring - Wikipedia'dan ma'lumot olasiz")
    print("=" * 50)
    
    # 36. BOTNI POLLING ORQALI ISHGA TUSHIRISH (XATOLIK BILAN ISHLASH)
    try:
        await dp.start_polling(bot)  # Botni doimiy ishlash rejimiga o'tkazish (yangi xabarlarni so'rov qilib turish)
    except KeyboardInterrupt:  # Agar foydalanuvchi Ctrl+C bossa
        print("\n❌ Bot to'xtatildi")  # Xabarni chiqarish
    except Exception as e:  # Boshqa xatolar
        print(f"❌ Botda xatolik: {e}")  # Xatolikni ko'rsatish
    finally:  # Har qanday holatda ham bajariladigan qism
        await bot.session.close()  # Botning internet ulanishini tozalash va yopish

# 37. DASTURNI ISHGA TUSHIRISH
if __name__ == '__main__':  # Agar bu fayl to'g'ridan-to'g'ri ishga tushirilgan bo'lsa (import qilinmagan bo'lsa)
    try:
        asyncio.run(main())  # Asinxron main() funksiyasini ishga tushirish
    except KeyboardInterrupt:  # Agar foydalanuvchi Ctrl+C bossa
        print("\n❌ Dastur to'xtatildi")  # Xabarni chiqarish va to'xtatish