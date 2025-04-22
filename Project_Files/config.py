from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")