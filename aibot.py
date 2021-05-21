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


notes = {}

class Company(StatesGroup):
    inn = State()
    invoise = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):

    keyboard = await keyboards.main_keyboard()
    await message.answer(f"Дорогой клиент, вас приветствует информационный бот компании {config.COMPANY}!\n"
                         "Данный бот был создан для быстрого получения статуса вашего заказа.\n"
                         "Для продолжения нажмите клавишу 'Узнать о заказа'", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getInvoice')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):

    keyboard = await keyboards.invoice_keyboard()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Кто вы:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getInvoiceCompany')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):
    await Company.inn.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите пожалуйства ИНН вашей фирмы:')


@dp.callback_query_handler(lambda c: c.data == 'getInvoicePerson')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Функционал для получиения статуса заказа для физических лиц\n'
                                                        'Еще в разработке')

# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(lambda c: c.data == 'getContacts')
async def process_callback_getInvouce(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, config.CONTACT)


@dp.message_handler(lambda message: message.text.isdigit(), state=Company.inn)
async def process_inn(message: types.Message, state: FSMContext):
    """
    Process inn Company
    """
    await state.update_data(inn=int(message.text))

    await Company.next()
    await message.reply("Введите последних 5 цифр вашего заказа:")


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


@dp.message_handler(lambda message: message.text.isdigit(), state=Company.invoise)
async def process_invoise(message: types.Message, state: FSMContext):
    # Update state and data
    await state.update_data(invoise=int(message.text))


    async with state.proxy() as data:

        inn = str(md.bold(data['inn']))
        invoise = str(md.bold(data['invoise']))

        all_invoce = pb.get_invoice(inn.replace("*", ""), invoise.replace("*", ""))

        markup = await keyboards.main_keyboard()
        await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f'По организации {all_invoce[2]} сейчас в работе {all_invoce[0]} заказов'),
                    md.text(f'Статус заказа {invoise.replace("*", "")}: {all_invoce[1]} ', ),
                    sep='\n',
                ),
                reply_markup=markup
        )

    # Finish conversation
    await state.finish()


if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True) #skip_updates=True позволяет пропустить накопившиеся входящие сообщения