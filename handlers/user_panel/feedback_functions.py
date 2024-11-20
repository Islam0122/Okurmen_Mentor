from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from filter.chat_types import ChatTypeFilter, IsAdmin
from handlers.user_panel.start_functions import user_preferences
from keyboard.inline import *
from message_text.text import messages, cancel

feedback_private_router = Router()
feedback_private_router.message.filter(ChatTypeFilter(['private']))


class FeedbackState(StatesGroup):
    WaitingForReview = State()


@feedback_private_router.callback_query(F.data.startswith("feedback"))
async def send_review_request_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')

    await query.message.edit_caption(
        caption=messages[language]['review'],
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(FeedbackState.WaitingForReview)


@feedback_private_router.callback_query(F.data == "cancel_feedback")
async def cancel_feedback(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    await state.clear()
    await query.message.edit_caption(caption=messages[language]['request_canceled'],
                                     reply_markup=start_functions_keyboard(language))


@feedback_private_router.callback_query(F.data == "cancel_create_feedback")
async def cancel_feedback(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    await state.clear()
    photo_path = 'media/welcome_img.jpg'
    await query.message.answer_photo(
        photo=types.FSInputFile(photo_path),
        caption=messages[language]['request_canceled'],
        reply_markup=start_functions_keyboard(language))


@feedback_private_router.message(FeedbackState.WaitingForReview)
async def process_review(message: types.Message, state: FSMContext, bot: Bot):
    language = user_preferences.get(message.from_user.id, {}).get('language', 'ru')
    group_id = bot.group_id  # ID группы для получения отзывов

    # Проверка на содержание текста или медиа
    if message.text:
        if message.text.lower() == cancel[language].lower():
            await state.clear()
            await message.answer(messages[language]['request_canceled'], reply_markup=return_menu_keyboard(language))
            return

        # Если отзыв не пустой, отправляем его
        user_info = f"{message.from_user.first_name}"
        if message.from_user.last_name:
            user_info += f" {message.from_user.last_name}"
        if message.from_user.username:
            user_info += f" (@{message.from_user.username})"

        review_text = message.text
        review_message = f"💬 Отзыв от {user_info}:\n\n{review_text}"
        await state.clear()
        # Отправка отзыва в группу
        await bot.send_message(chat_id=group_id, text=review_message)
        await message.answer(messages[language]['review_thanks'], reply_markup=return_menu_keyboard(language))
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_create_feedback"))
        await message.answer(messages[language]['review_invalid'], reply_markup=keyboard.as_markup())
