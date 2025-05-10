import asyncio

from aiogram import Bot, Dispatcher
from handlers import router
from config import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN)  # Используем реальный токен
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is off')
