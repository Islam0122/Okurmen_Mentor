from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from filter.chat_types import ChatTypeFilter, IsAdmin
from handlers.user_panel.ai_function import sent_prompt_and_get_response
from handlers.user_panel.start_functions import user_preferences
from keyboard.inline import *
from message_text.text import messages, cancel


ai_help_private_router = Router()
ai_help_private_router.message.filter(ChatTypeFilter(['private']))


# Переименованный класс состояния
class AiAssistanceState(StatesGroup):
    WaitingForReview = State()


@ai_help_private_router.callback_query(F.data.startswith("ai_help"))
async def send_review_request_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'kgz')

    await query.message.edit_caption(
        caption=messages[language]['ai_help_message'],
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(AiAssistanceState.WaitingForReview)  # Используем новое имя состояния


@ai_help_private_router.callback_query(F.data == "cancel_ai_help")
async def cancel_feedback(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    await state.clear()
    await query.message.edit_caption(caption=messages[language]['request_canceled'],
                                     reply_markup=start_functions_keyboard(language))


# Переименованная функция
@ai_help_private_router.message(AiAssistanceState.WaitingForReview)  # Используем новое имя класса состояния
async def process_help_request(message: types.Message, state: FSMContext, bot: Bot):
    language = user_preferences.get(message.from_user.id, {}).get('language', 'ru')

    if message.text:
        generated_help = sent_prompt_and_get_response(message.text, language)
        await message.answer(generated_help, reply_markup=ReplyKeyboardRemove())
        await state.clear()
        await message.answer(messages[language]['review_sent'], reply_markup=start_functions_keyboard(language))
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_create_feedback"))
        await message.answer(messages[language]['review_invalid'], reply_markup=keyboard.as_markup())
