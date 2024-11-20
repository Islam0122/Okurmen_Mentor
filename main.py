import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from handlers.user_panel.ai_help import ai_help_private_router
from handlers.user_panel.feedback_functions import feedback_private_router
from handlers.user_panel.send_help_request import send_help_request_private_router
from handlers.user_panel.start_functions import start_functions_private_router

load_dotenv(find_dotenv())

from common.bot_cmds_list import private
from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy="http://proxy.server:3128")

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = [5627082052,]
bot.group_id = os.getenv('group_id')


dp = Dispatcher()

dp.include_router(start_functions_private_router)
dp.include_router(feedback_private_router)
dp.include_router(send_help_request_private_router)
dp.include_router(ai_help_private_router)
# dp.include_router(unknown_private_router)


async def on_startup(bot):
    await bot.send_message(bot.my_admins_list[0], "Сервер успешно запущен! 😊 Привет, босс!")


async def on_shutdown(bot):
    await bot.send_message(bot.my_admins_list[0], "Сервер остановлен. 😔 Проверьте его состояние, босс!")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
