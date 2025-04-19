import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Твой токен бота
TOKEN = "7600848578:AAGmButWfDlPMCr5i0uhisHIKLVsKrDJRXw"

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🩺 Терапевт"), KeyboardButton(text="🦷 Стоматология")],
        [KeyboardButton(text="👁 Офтальмология"), KeyboardButton(text="❤️ Кардиология")],
        [KeyboardButton(text="📞 Администратор"), KeyboardButton(text="📍 Контакты")],
        [KeyboardButton(text="⚠️ Острая боль")]
    ],
    resize_keyboard=True
)

# Ключевые слова
SCENARIOS = {
    "терапевт": ["терапевт", "врач", "простуда", "температура", "болит горло"],
    "стоматология": ["стоматолог", "зуб", "болит зуб", "кариес", "зубной"],
    "офтальмология": ["офтальмолог", "глаз", "зрение", "плохо вижу"],
    "кардиология": ["кардиолог", "сердце", "давление", "тахикардия"],
    "острая боль": ["острая боль", "очень больно", "срочно", "экстренно"]
}

# Ответы
RESPONSES = {
    "терапевт": "🩺 Вы записаны к терапевту! Врач скоро подключится.",
    "стоматология": "🦷 Вас перевели в отдел стоматологии. Ожидайте ответа специалиста.",
    "офтальмология": "👁 Вас перевели в офтальмологию. Врач свяжется с вами в ближайшее время.",
    "кардиология": "❤️ Вас переключили на кардиолога. Ожидайте ответа.",
    "администратор": "📞 Сейчас вам перезвонит Администратор.",
    "контакты": "📍 Наш адрес: ул. Пушкина, д. Колотушкина. Телефон: +7 (900) 123-45-67",
    "острая боль": "⚠️ Срочный вызов врача! Мы немедленно передадим ваш запрос!"
}

# Функция для поиска категории по тексту
def find_category(text: str):
    text = text.lower()
    for category, keywords in SCENARIOS.items():
        if any(keyword in text for keyword in keywords):
            return category
    if "администратор" in text:
        return "администратор"
    if "контакт" in text or "адрес" in text:
        return "контакты"
    return None

# Обработчик старта
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте! Чем можем помочь?", reply_markup=menu)

# Обработчик сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    category = find_category(user_text)
    if category:
        await message.answer(RESPONSES[category], reply_markup=menu)
    else:
        await message.answer("Извините, я не понял ваш запрос. Пожалуйста, выберите опцию из меню.", reply_markup=menu)

# Запуск
async def main():
    logger.info("Starting bot...")  # Вставили сюда лог перед стартом
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
