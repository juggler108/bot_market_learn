from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_market_learn.core.keyboards.text_button import get_button_name
from bot_market_learn.core.others.db_request import Request
from bot_market_learn.core.others.state_user import States


async def get_date(message: Message, state: FSMContext, request: Request):
    await message.answer(f"Приятно познакомиться {message.text}, теперь выберите время")
    await state.update_data(name=message.text)
    await state.set_state(States.state_date)

    print(await state.get_data())


async def get_name(message: Message, state: FSMContext, request: Request):
    await message.answer(text=f"Привет! Я помощник салона красоты Шафран. Как я могу к тебе обращаться?",
                         reply_markup=await get_button_name(message.from_user.first_name))
    await state.set_state(States.state_name)
