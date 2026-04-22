# ======================== KERAKLI KUTUBXONALARNI YUKLASH ========================
# asyncio - asinxron dasturlash uchun (bir vaqtning o'zida bir nechta ishni bajarish)
import asyncio
# logging - xatoliklarni va jarayonlarni qayd qilish uchun
import logging
# aiogram - Telegram bot yaratishning eng kuchli kutubxonasi
from aiogram import Bot, Dispatcher, types
# Command - botga komanda yozilganda ishlaydigan filter
from aiogram.filters import Command
# ReplyKeyboardMarkup, KeyboardButton - tugmalar yaratish uchun
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# ======================== BOT TOKENI ========================
# Bu token botning "passporti" - har bir botning o'ziga xos identifikatori
# Token orqali Telegram botga ulanish va uni boshqarish mumkin
API_TOKEN = '8577685040:AAHhEi0vAV8_GXSu830GaFp5JDLBSWE_gn0'


# ======================== LOGINGNI SOZLASH ========================
# Bu qator botning nima qilayotganini konsolda ko'rsatadi
# INFO darajasi - muhim ma'lumotlarni ko'rsatadi (xatoliklar, ulanishlar va h.k.)
logging.basicConfig(level=logging.INFO)

# ======================== BOT OBYEKTLARINI YARATISH ========================
# Bot obyekti - botning o'zi. Token orqali Telegram bilan bog'lanadi
bot = Bot(token=API_TOKEN)
# Dispatcher - barcha xabarlarni qabul qiladi va ularni to'g'ri handlerlarga yo'naltiradi
dp = Dispatcher()


# ======================== TUGMALAR KLAVIATURASINI YARATISH ========================
# ReplyKeyboardMarkup - foydalanuvchi yozish o'rniga tugmachalarni bosishi uchun
# Bu oddiy tugmalar (inline tugmalar emas)
keyboard1 = ReplyKeyboardMarkup(
    # keyboard - tugmalar qatorini belgilaydi. Har bir [] - bir qator
    keyboard=[
        # Birinchi qator - faqat "Salom" tugmasi
        [KeyboardButton(text="Salom")],
        # Ikkinchi qator - "Xayr" tugmasi
        [KeyboardButton(text="Xayr")],
        # Uchinchi qator - "Salomat" tugmasi
        [KeyboardButton(text="Salomat")],
        # To'rtinchi qator - "Omonmisiz" tugmasi
        [KeyboardButton(text="Omonmisiz")],
        # Beshinchi qator - "Chuvak" tugmasi
        [KeyboardButton(text="Chuvak")]
    ],
    # resize_keyboard=True - tugmalarni kichik va chiroyli qiladi
    resize_keyboard=True,
    # one_time_keyboard=False - tugmalar har doim ko'rinib turadi (bir marta emas)
    one_time_keyboard=False
)


# ======================== START KOMANDASI HANDLERI ========================
# @dp.message(Command("start")) - bu dekorator. /start komandasi yozilganda ishlaydi
@dp.message(Command("start"))
async def start_message(message: types.Message):
    # message.chat.id - foydalanuvchi bilan suhbatning ID raqami
    # message.answer() - foydalanuvchiga javob yuborish
    await message.answer(
        # Foydalanuvchiga ko'rinadigan matn
        "Salom siz! /start tugmasini bosdingiz!",
        # reply_markup=keyboard1 - tugmalarni ham birga yuborish
        reply_markup=keyboard1
    )


# ======================== MATNLI XABARLAR HANDLERI ========================
# @dp.message() - hech qanday filtersiz, har qanday matnli xabarni ushlaydi
@dp.message()
async def send_text(message: types.Message):
    # message.text - foydalanuvchi yozgan matn
    # .lower() - matnni kichik harflarga o'tkazadi (SALOM -> salom)
    # agar matn bo'lmasa (masalan rasm bo'lsa) "" bo'ladi
    text = message.text.lower() if message.text else ""
    
    # ========== SALOM ==========
    # Agar foydalanuvchi "salom" yoki "Salom" yozsa (kichik-katta farqi yo'q)
    if text == 'salom':
        # Javob yuborish
        await message.answer('Salom chuvak')
    
    # ========== XAYR ==========
    # Agar foydalanuvchi "xayr" yozsa
    elif text == 'xayr':
        await message.answer('Uydilaga salom!')
    
    # ========== SALOMAT ==========
    elif text == 'salomat':
        await message.answer('Uydila uydami')
    
    # ========== OMONMISIZ ==========
    elif text == 'omonmisiz':
        await message.answer('pul kam ukam')
    
    # ========== CHUVAK ==========
    # "chuvak" tugmasi bosilganda video yuborish
    elif text == 'chuvak':
        # try - xatolik bo'lishi mumkin bo'lgan kodni sinab ko'rish
        try:
            # 'video.mp4' faylini o'qish rejimida ochish (rb - read binary)
            video = open('video.mp4', 'rb')
            # bot.send_video - video fayl yuborish
            # await - asinxron funksiyani kutish
            await bot.send_video(message.chat.id, video)
            # Faylni yopish (xotirani bo'shatish)
            video.close()
            
            
            # Yoki video ID orqali yuborish (agar video avval yuborilgan bo'lsa)
            # file_id - Telegram serveridagi videoning manzili
            file_id = 'AAAaaaZZZzzz'
            await bot.send_video(message.chat.id, file_id)
            
        # except - agar xatolik yuz bersa (masalan video topilmasa)
        except FileNotFoundError:
            # Foydalanuvchiga xatolik haqida xabar berish
            await message.answer("Video fayl topilmadi!")
        # Har qanday boshqa xatolik uchun
        except Exception as e:
            # Xatolik matnini foydalanuvchiga ko'rsatish
            await message.answer(f"Xatolik yuz berdi: {e}")


# ======================== BOTNI ISHGA TUSHIRISH ========================
# async def main() - asinxron asosiy funksiya
async def main():
    # Konsolga xabar chiqarish
    print("Bot ishga tushdi...")
    # dp.start_polling(bot) - botni ishga tushirish va xabarlarni kuta boshlash
    await dp.start_polling(bot)


# ======================== DASTURNI ISHGA TUSHIRISH ========================
# if __name__ == "__main__" - bu fayl to'g'ridan-to'g'ri ishga tushirilganda
if __name__ == "__main__":
    # asyncio.run(main()) - asinxron main() funksiyasini ishga tushirish
    asyncio.run(main())