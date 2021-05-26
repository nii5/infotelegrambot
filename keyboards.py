from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButtonPollType, PollType


async def main_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_status = InlineKeyboardButton('Заказ', callback_data='getInvoice')
    button_contacts = InlineKeyboardButton('Контакты', callback_data='getContacts')
    button_site = InlineKeyboardButton('Интернет-магазин', url='https://shop.pneumax.ru/')
    button_map = InlineKeyboardButton('Построить маршрут Яндекс', url='https://maps.yandex.ru/?pt=37.41916085876312,55.911840227450554&z=15&l=map')
    # button_person = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    # button_location = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    keyboard.row(button_status, button_contacts)
    keyboard.add(button_site)
    keyboard.add(button_map)

    return keyboard


async def invoice_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_company = InlineKeyboardButton('Юр.лицо, ИП', callback_data='getInvoiceCompany')
    button_person = InlineKeyboardButton('Физ.лицо', callback_data='getInvoicePerson')
    # button_location = InlineKeyboardButton('Физ.лицо', callback_data='getPerson')
    keyboard.row(button_company, button_person)

    return keyboard

async def confirmation_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_company = InlineKeyboardButton('Да', callback_data='getСonfirmationYes')
    button_person = InlineKeyboardButton('Нет', callback_data='getConfirmationNo')

    keyboard.row(button_company, button_person)

    return keyboard

#
async def admistrator_menu_keyboard():

    keyboard = InlineKeyboardMarkup()
    button_company = InlineKeyboardButton('Написать новость', callback_data='getNewsMesseng')
    button_person = InlineKeyboardButton('Подписчики', callback_data='getAllUsers')

    keyboard.add(button_company, button_person)

    return keyboard


async def cancel_button_keyboard():

    button_cancel = KeyboardButton('/cancel')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_cancel)

    return keyboard
