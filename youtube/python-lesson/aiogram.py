# 1. OS MODULI - Operatsion tizim bilan ishlash uchun
import os  # Fayl va papkalar bilan ishlash (yaratish, o'chirish, nomlash, o'lchamni tekshirish)

# 2. RE MODULI - Muntazam ifodalar bilan ishlash uchun
import re  # Matn ichida qidirish va tozalash (fayl nomlaridan keraksiz belgilarni olib tashlash)

# 3. ASYNCIO MODULI - Asinxron dasturlash uchun
import asyncio  # Botning bir vaqtning o'zida bir nechta foydalanuvchiga xizmat ko'rsatishi uchun

# 4. LOGGING MODULI - Xatoliklarni qayd qilish uchun
import logging  # Botning ishlashi davomida yuz beradigan hodisalarni konsolga yoki faylga yozish

# 5. AIOGRAM MODULI - Telegram bot yaratish uchun asosiy kutubxona
from aiogram import Bot, Dispatcher, types  # Bot - bot obyekti, Dispatcher - xabarlarni boshqaruvchi, types - Telegram xabarlar turlari

# 6. AIOGRAM FILTERS - Xabarlarni filtrlash uchun
from aiogram.filters import Command  # /start, /help kabi buyruqlarni aniqlash uchun filter

# 7. AIOGRAM TYPES - Fayl jo'natish uchun
from aiogram.types import FSInputFile  # Lokal faylni Telegramga jo'natish uchun maxsus klass

# 8. YT_DLP MODULI - YouTube videolarni yuklab olish uchun
from yt_dlp import YoutubeDL  # YouTube va boshqa saytlardan video/audio yuklab olish uchun kuchli kutubxona

# 9. TOKEN - Botning maxsus kaliti
TOKEN = "8577685040:AAHhEi0vAV8_GXSu830GaFp5JDLBSWE_gn0"  # Botfather dan olingan bot tokeni

# 10. YUKLAB OLISH PAPKASI
DOWNLOAD_DIR = "downloads"  # Yuklab olingan videolar saqlanadigan papka nomi

# 11. FAYL HAJMI CHEGARASI
LIMIT = 50 * 1024 * 1024  # Telegram videolarni yuborish chegarasi - 50 megabayt (50 * 1024KB * 1024B)

# 12. LOGGING SOZLAMALARI
logging.basicConfig(level=logging.INFO)  # INFO darajadagi va undan yuqori xabarlarni konsolga chiqarish
logger = logging.getLogger(__name__)  # Ushbu modul uchun maxsus logger obyekti yaratish

# 13. BOT VA DISPATCHER OBYEKTLARI
bot = Bot(TOKEN)  # Berilgan token bilan bot obyektini yaratish
dp = Dispatcher()  # Barcha kelgan xabarlarni handlerlarga yo'naltiruvchi obyekt

# 14. LOGGERNI O'CHIRISH KLASSI - yt-dlp ning keraksiz chiqindilarini bostirish uchun
class QuietLogger:  # yt-dlp kutubxonasining log chiqarishini o'chiruvchi klass
    def debug(self, msg): pass  # Debug xabarlarini e'tiborsiz qoldirish
    def warning(self, msg): pass  # Warning xabarlarini e'tiborsiz qoldirish
    def error(self, msg): pass  # Error xabarlarini e'tiborsiz qoldirish (biz o'zimiz boshqaramiz)

# 15. FAYL NOMINI TOZALASH FUNKSIYASI
def clean_filename(name: str) -> str:
    # Fayl nomida bo'lishi mumkin bo'lgan xavfli belgilarni olib tashlash
    name = re.sub(r'[<>:"/\\|?*]', '', name)  # Windows fayl tizimida ruxsat etilmagan belgilarni o'chirish
    name = re.sub(r'[^A-Za-z0-9а-яА-ЯёЁ\-_(). ]', '', name)  # Faqat harflar, raqamlar va ba'zi belgilarni qoldirish
    return name.strip()  # Boshi va oxiridagi bo'sh joylarni olib tashlash

# 16. VIDEONI YUKLAB OLISH FUNKSIYASI
async def try_download(url: str, format_spec: str):
    """YouTube videoni berilgan formatda yuklab olish"""
    try:
        # yt-dlp sozlamalari
        ydl_opts = {
            'quiet': True,  # Chiqishni minimallashtirish
            'no_warnings': True,  # Ogohlantirishlarni chiqarmaslik
            'logger': QuietLogger(),  # O'zimizning jim loggerimizni ishlatish
            'noplaylist': True,  # Faqat bitta videoni yuklab olish (pleylist emas)
            'format': format_spec,  # Video formatini tanlash (masalan: best, mp4, 720p)
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',  # Faylni saqlash joyi va nomi (video sarlavhasi bilan)
            'restrictfilenames': True,  # Fayl nomini xavfsiz qilish (keraksiz belgilarni olib tashlash)
        }
        
        # yt-dlp obyektini yaratish va videoni yuklab olish
        with YoutubeDL(ydl_opts) as ydl:
            # Asinxron tarzda (boshqa foydalanuvchilarni to'xtatmasdan) videoni yuklab olish
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            # Yuklab olingan faylning to'liq manzilini olish
            filename = ydl.prepare_filename(info)
            
            # 17. FAYLNI TEKSHIRISH - Agar fayl mavjud bo'lmasa, boshqa kengaytmalarni tekshirish
            if not os.path.exists(filename):
                base = os.path.splitext(filename)[0]  # Fayl nomini kengaytmasiz olish
                # Turli video kengaytmalarni tekshirish
                for ext in ['.mp4', '.webm', '.mkv', '.avi']:
                    test_file = base + ext  # Kengaytma qo'shib ko'rish
                    if os.path.exists(test_file):
                        filename = test_file  # Topilgan faylni ishlatish
                        break
                else:
                    return None, None  # Hech qanday fayl topilmasa
            
            # 18. FAYL NOMINI TOZALASH
            clean = clean_filename(os.path.basename(filename))  # Fayl nomini tozalash
            clean_path = os.path.join(DOWNLOAD_DIR, clean)  # To'liq manzil yaratish
            
            # 19. FAYLNI QAYTA NOMLASH (agar kerak bo'lsa)
            if clean_path != filename:  # Agar eski nom yangidan farq qilsa
                if os.path.exists(clean_path):
                    os.remove(clean_path)  # Agar yangi nomli fayl mavjud bo'lsa, o'chirish
                os.rename(filename, clean_path)  # Faylni tozalangan nom bilan qayta nomlash
                filename = clean_path  # Yangi manzilni saqlash
            
            return filename, info  # Fayl manzili va video ma'lumotlarini qaytarish
            
    except Exception as e:  # Agar yuklab olishda xatolik bo'lsa
        logger.error(f"Download error: {e}")  # Xatolikni logga yozish
        return None, None  # Hech narsa topilmadi

# 20. XABARNI XAVFSIZ O'CHIRISH FUNKSIYASI
async def safe_delete_message(message: types.Message):
    """Xabarni xavfsiz o'chirish (xatolik yuz bersa ham)"""
    try:
        if message:  # Agar xabar mavjud bo'lsa
            await message.delete()  # Xabarni o'chirish
    except Exception as e:  # Xatolik yuz bersa
        logger.warning(f"Could not delete message: {e}")  # Ogohlantirishni logga yozish (davom etish)

# 21. START BUYRUG'I HANDLERI
@dp.message(Command("start"))  # /start buyrug'iga javob beruvchi dekorator
async def send_welcome(msg: types.Message):
    await msg.answer(  # Foydalanuvchiga salomlashish xabari
        "🎬 YouTube video yuklab olish boti\n\n"
        "Video linkini yuboring. Bot eng mos formatda yuklab beradi.\n"
        "Cheklov: 50MB gacha"
    )

# 22. HELP BUYRUG'I HANDLERI
@dp.message(Command("help"))  # /help buyrug'iga javob
async def send_help(msg: types.Message):
    await msg.answer(  # Yordam xabari
        "🤖 Botdan foydalanish:\n\n"
        "1. YouTube video linkini yuboring\n"
        "2. Bot avtomatik ravishda eng mos sifatni tanlaydi\n"
        "3. Video 50MB dan kichik bo'lsa yuboriladi\n\n"
        "Agar video yuklanmasa:\n"
        "• Video 50MB dan katta bo'lishi mumkin\n"
        "• Video xususiy yoki o'chirilgan bo'lishi mumkin"
    )

# 23. ASOSIY HANDLER - Barcha matnli xabarlar uchun (video linklari)
@dp.message()  # Hech qanday filter yo'q - barcha matnli xabarlar shu yerga keladi
async def download_video(msg: types.Message):
    url = msg.text.strip()  # Foydalanuvchi yuborgan matnni olib, bo'sh joylarni tozalash
    
    # 24. URL TEKSHIRISH - Bu haqiqatan ham YouTube linkimi?
    if not (url.startswith(("http://", "https://", "www.")) or "youtu.be" in url or "youtube.com" in url):
        return await msg.answer("❌ Iltimos, to'g'ri YouTube video linki yuboring.")  # Xatolik xabari
    
    status_msg = None  # Status xabarini saqlash uchun o'zgaruvchi
    try:
        status_msg = await msg.answer("⏳ Video yuklanmoqda... Bu bir necha daqiqa vaqt olishi mumkin.")  # Yuklanayotganini bildirish
    except:
        pass  # Agar xabar yuborishda xatolik bo'lsa, davom etish
    
    # 25. VIDEO FORMATLARI RO'YXATI (eng yaxshidan eng yomonga)
    formats = [
        "best[height<=720][ext=mp4]/best[height<=720]/best[ext=mp4]",  # Eng yaxshi 720p MP4
        "best[height<=480][ext=mp4]/best[height<=480]/best[ext=mp4]",  # 480p MP4
        "best[height<=360][ext=mp4]/best[height<=360]/best[ext=mp4]",  # 360p MP4
        "best[height<=240][ext=mp4]/best[height<=240]/best[ext=mp4]",  # 240p MP4
        "worst[ext=mp4]/worst",  # Eng yomon MP4 (kichik hajm)
        "best[ext=mp4]",  # Eng yaxshi MP4 (ixtiyoriy sifat)
        "best"  # Eng yaxshi video (ixtiyoriy format)
    ]
    
    # 26. HAR BIR FORMATNI SINAB KO'RISH
    for fmt in formats:
        filepath, info = await try_download(url, fmt)  # Videoni shu formatda yuklab olishga urinish
        
        # 27. AGAR VIDEO MUVAFfaQIYATLI YUKLAB OLINSA
        if filepath and os.path.exists(filepath):
            try:
                size = os.path.getsize(filepath)  # Fayl hajmini o'lchash (baytlarda)
                
                # 28. HACM TEKSHIRISH - 50MB dan kichikmi?
                if size <= LIMIT:
                    title = info.get("title", "Video")  # Video sarlavhasini olish
                    if len(title) > 200:  # Agar sarlavha juda uzun bo'lsa
                        title = title[:197] + "..."  # Qisqartirish
                    
                    # 29. FAYLNI YUBORISHGA TAYYORLASH
                    video_file = FSInputFile(filepath)  # Lokal faylni Telegram formatiga o'tkazish
                    
                    # 30. STATUS XABARINI O'CHIRISH
                    await safe_delete_message(status_msg)  # "Yuklanmoqda..." xabarini o'chirish
                    
                    # 31. VIDEONI YUBORISH
                    await msg.answer_video(
                        video_file,  # Video fayli
                        caption=f"📹 {title}\n💾 {(size / (1024*1024)):.1f} MB",  # Rasm ostidagi matn (sarlavha va hajm)
                        supports_streaming=True  # Telegram'da to'g'ridan-to'g'ri ko'rish imkoniyati
                    )
                    
                    # 32. LOYIHALIK FAYLNI O'CHIRISH
                    os.remove(filepath)  # Yuklab olingan faylni diskdan o'chirish
                    return  # Muvaffaqiyatli yuborildi, funksiyani to'xtatish
                    
                else:  # Agar video 50MB dan katta bo'lsa
                    os.remove(filepath)  # Faylni o'chirish (kerak emas)
                    continue  # Keyingi formatni sinab ko'rish
                    
            except Exception as e:  # Yuborishda xatolik bo'lsa
                logger.error(f"Send error: {e}")  # Xatolikni logga yozish
                if os.path.exists(filepath):  # Agar fayl mavjud bo'lsa
                    try:
                        os.remove(filepath)  # Faylni o'chirishga urinish
                    except:
                        pass  # O'chirishda xatolik bo'lsa, e'tiborsiz qoldirish
                continue  # Keyingi formatni sinab ko'rish
    
    # 33. HAMMA FORMATLAR SINAB KO'RILDI, HECH BIRI ISHLAMADI
    await safe_delete_message(status_msg)  # Status xabarini o'chirish
    
    # 34. XATOLIK HAQIDA XABAR YUBORISH
    await msg.answer(
        "❌ Kechirasiz, video yuklab bo'lmadi.\n\n"
        "Sabablari:\n"
        "• Video 50MB dan katta\n"
        "• Video xususiy yoki o'chirilgan\n"
        "• Video formati qo'llab-quvvatlanmaydi\n\n"
        "Boshqa video yoki kichikroq hajmdagi videoni sinab ko'ring."
    )

# 35. ASOSIY ASINXRON FUNKSIYA - Botni ishga tushirish
async def main():
    """Botni ishga tushirish"""
    # Papkalarni yaratish (agar mavjud bo'lmasa)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Yuklab olish papkasini yaratish (exist_ok=True - mavjud bo'lsa xatolik chiqarmaydi)
    
    print("Bot ishga tushdi...")  # Konsolga chiqarish
    print("Bot @username bilan Telegramda ishga tayyor")
    
    # Botni polling orqali ishga tushirish
    await dp.start_polling(bot)  # Botni doimiy ishlash rejimiga o'tkazish (yangi xabarlarni so'rov qilib turish)

# 36. DASTURNI ISHGA TUSHIRISH
if __name__ == "__main__":
    asyncio.run(main())  # Asinxron main() funksiyasini ishga tushirish