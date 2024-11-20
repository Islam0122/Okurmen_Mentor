from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from message_text.text import *


def start_functions_keyboard(language: str):
    """Функция для создания клавиатуры."""
    keyboard = InlineKeyboardBuilder()

    # Добавление кнопок с текстом и callback_data
    keyboard.add(InlineKeyboardButton(
        text=f"🆘 {button_texts[language]['send_help_request']}",
        callback_data='send_help_request'
    ))

    keyboard.add(InlineKeyboardButton(
        text=f"ℹ️ {button_texts[language]['about_bot']}",
        callback_data='about_bot'
    ))
    keyboard.add(InlineKeyboardButton(
        text=f"❓ {button_texts[language]['help']}",
        callback_data='help'
    ))
    keyboard.add(InlineKeyboardButton(
        text=f"⭐ {button_texts[language]['leave_review']}",
        callback_data='feedback'
    ))

    keyboard.add(InlineKeyboardButton(
        text=f"🤖 {button_texts[language]['ai_help']}",
        callback_data='ai_help'
    ))
    keyboard.add(InlineKeyboardButton(
        text=f"🌐 {button_texts[language]['select_language']}",
        callback_data='change_language'
    ))
    # Настройка кнопок: по 2 в строке
    return keyboard.adjust(1,2,1,1).as_markup()


def return_menu_keyboard(language):
    """Функция для создания клавиатуры с кнопкой 'Вернуться в меню'."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))
    return keyboard.as_markup()


def return_menu_from_about_keyboard(language):
    """Функция для создания клавиатуры с кнопкой 'Вернуться в меню'."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=texts['leave_review'], callback_data='feedback'))
    keyboard.add(InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))
    return keyboard.adjust(1,1).as_markup()


def language_selection_keyboard(language: str):
    """Функция для создания клавиатуры выбора языка."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language_en"),
        InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="set_language_kgz"),
        InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))

    return keyboard.adjust(3).as_markup()


def get_cancel_keyboard(language):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_feedback"))
    return keyboard.as_markup()

