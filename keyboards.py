from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButtonPollType, PollType


async def main_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_status = InlineKeyboardButton('Узнать о заказе', callback_data='getInvouce')
    button_contacts = InlineKeyboardButton('Наш контакты', callback_data='getContacts')
    button_person = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    button_location = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    keyboard.row(button_status, button_person, button_contacts)

    return keyboard
