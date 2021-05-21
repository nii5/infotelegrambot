from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButtonPollType, PollType


async def main_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_status = InlineKeyboardButton('Заказ', callback_data='getInvoice')
    button_contacts = InlineKeyboardButton('Контакты', callback_data='getContacts')
    # button_person = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    # button_location = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    keyboard.row(button_status, button_contacts)

    return keyboard


async def invoice_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_company = InlineKeyboardButton('Юр.лицо, ИП', callback_data='getInvoiceCompany')
    button_person = InlineKeyboardButton('Физ.лицо', callback_data='getInvoicePerson')
    # button_location = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    keyboard.row(button_company, button_person)

    return keyboard
