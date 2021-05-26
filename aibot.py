import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import pb
import keyboards
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


class Company(StatesGroup):
    inn = State()
    invoise = State()


class Newspneumax(StatesGroup):
    text = State()

class Pesrson(StatesGroup):
    invoise = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):

    keyboard = await keyboards.main_keyboard()
    await message.answer(f"Вас приветствует компания {config.COMPANY}.\n"
                         "Чтобы получить информацию о статусе заказа, нажмите 'Заказ '", reply_markup=keyboard)


@dp.message_handler(commands=["adminmenumesseng"])
async def cmd_start(message: types.Message):

    keyboard = await keyboards.admistrator_menu_keyboard()
    await message.answer(f"Админское меню данного бота", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text is not None, state=Newspneumax.text)
async def process_callback_news_all_users(message: types.Message, state: FSMContext):
    # Update state and data
    await state.update_data(text=message.text)

    if message.text != '/cancel':
        markup = await keyboards.main_keyboard()
        all_users = pb.get_all_users()
        for i in all_users:
            try:
                await bot.send_message(i[0], message.text, reply_markup=markup)

            except:
                print("Пользователь удалился")

    await state.finish()



@dp.callback_query_handler(lambda c: c.data == 'getAllUsers')
async def process_callback_getAllUsers(callback_query: types.CallbackQuery):

    keyboard = await keyboards.admistrator_menu_keyboard()
    alluser = len(pb.get_all_users())
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Сейчас на бота подписано {alluser} человек', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getNewsMesseng')
async def process_callback_getNewsMesseng(callback_query: types.CallbackQuery):

    keyboard = await keyboards.cancel_button_keyboard()
    await Newspneumax.text.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Введите новость для рассылки:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getInvoice')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):

    keyboard = await keyboards.invoice_keyboard()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Получить информацию по заказу на:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getInvoiceCompany')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):
    userinn = pb.find_user(callback_query.from_user.id)
    if userinn[0][1] == 0:
        await Company.inn.set()
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Введите ИНН организации:')
    else:
        keyboard = await keyboards.confirmation_keyboard()
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f'Это ваш инн {userinn[0][1]}?', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getСonfirmationYes')
async def process_callback_getInvouce(callback_query: types.CallbackQuery, state: FSMContext):
    userinn = pb.find_user(callback_query.from_user.id)
    await Company.inn.set()
    await state.update_data(inn=int(userinn[0][1]))
    await Company.next()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите последние 5 цифр заказа:')


@dp.callback_query_handler(lambda c: c.data == 'getConfirmationNo')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):

    await Company.inn.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите ИНН организации:')


@dp.callback_query_handler(lambda c: c.data == 'getInvoicePerson')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)
    await Pesrson.invoise.set()
    await bot.send_message(callback_query.from_user.id, 'Введите последние 5 цифр заказа')

# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        keyboard = await keyboards.main_keyboard()
        await message.reply('Действие отменено.', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"Вас приветствует компания {config.COMPANY}.\n"
                             "Чтобы получить информацию о статусе заказа, нажмите 'Заказ '", reply_markup=keyboard)
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(lambda c: c.data == 'getContacts')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, config.CONTACT)


@dp.message_handler(lambda message: message.text.isdigit(), state=Company.inn)
async def process_inn(message: types.Message, state: FSMContext):
    """
    Process inn Company
    """
    await state.update_data(inn=int(message.text))
    pb.save_users_inn(message.from_user.id, int(message.text))

    await Company.next()
    await message.reply("Введите последние 5 цифр заказа:")


@dp.message_handler(lambda message: not message.text.isdigit() or len(message.text) < 10, state=Company.inn)
async def process_inn_invalid(message: types.Message):
    """
    If Company is invalid
    """
    return await message.reply("ИНН компании должен быть цифровой и более 9 цифр.\nВаш ИНН:")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Company.invoise)
async def process_invoise_invalid(message: types.Message):
    """
    If invoise is invalid
    """
    return await message.reply("Номер заказа должен быть цифровой.\nВведите последние 5 цифр заказа:")

@dp.message_handler(lambda message: not message.text.isdigit(), state=Pesrson.invoise)
async def process_invoise_invalid(message: types.Message):
    """
    If invoise is invalid
    """
    return await message.reply("Номер заказа должен быть цифровой.\nВведите последние 5 цифр заказа:")


@dp.message_handler(lambda message: message.text.isdigit(), state=Company.invoise)
async def process_invoise(message: types.Message, state: FSMContext):
    # Update state and data
    await state.update_data(invoise=int(message.text))


    async with state.proxy() as data:

        inn = str(md.bold(data['inn']))
        invoise = str(md.bold(data['invoise']))

        all_invoce = pb.get_invoice(inn.replace("*", ""), invoise.replace("*", ""))
        if all_invoce == False:
            text = f'По организации {inn} не найден заказ с номером {invoise} '
        else:
            products = pb.get_products(inn.replace("*", ""), invoise.replace("*", ""))
            text = f'Ваш заказ № {invoise.replace("*", "")}\n' \
                   f'Статус:  {all_invoce[0][3]}\n' \
                   f'Cумма заказа: {all_invoce[0][6]} \n' \
                   f'Доставка: {all_invoce[0][4]} \n' \
                   f'TK : {all_invoce[0][5]}\n\n' \
                   f'{products}'

        markup = await keyboards.main_keyboard()
        await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(text),
                    sep='\n',
                ),
                reply_markup=markup
        )

    # Finish conversation
    await state.finish()


@dp.message_handler(lambda message: message.text.isdigit(), state=Pesrson.invoise)
async def process_invoise_person(message: types.Message, state: FSMContext):
    # Update state and data
    await state.update_data(invoise=int(message.text))


    async with state.proxy() as data:

        invoise = str(md.bold(data['invoise']))

        all_invoce = pb.get_invoice_person(invoise.replace("*", ""))
        if all_invoce == False:
            text = f'Не найден заказ с номером {invoise} '
        else:
            products = pb.get_goods(invoise.replace("*", ""))
            text = f'Ваш заказ № {invoise.replace("*", "")}\n' \
                   f'Статус:  {all_invoce[0][3]}\n' \
                   f'Cумма заказа: {all_invoce[0][6]} \n' \
                   f'Доставка: {all_invoce[0][4]} \n' \
                   f'TK : {all_invoce[0][5]}\n\n' \
                   f'{products}'

        markup = await keyboards.main_keyboard()
        await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(text),
                    sep='\n',
                ),
                reply_markup=markup
        )

    # Finish conversation
    await state.finish()


if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True) #skip_updates=True позволяет пропустить накопившиеся входящие сообщения