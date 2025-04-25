import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from currency import Currency
import keyboards as kb
from exchange import get_exchange_rate, convert_currency

router = Router()
logger = logging.getLogger(__name__)

class ConversionState(StatesGroup):
    base_currency = State()
    target_currency = State()
    amount_input = State()

@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Welcome to the currency converter bot!", reply_markup=kb.main_button)

@router.message(F.text == 'Selection of popular currencies')
async def handle_popular_selection(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Please choose the base currency:", reply_markup=kb.base_button)
    await state.set_state(ConversionState.base_currency)

@router.message(F.text == 'Enter your currency')
async def handle_manual_currency_entry(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Please enter the base currency:")
    await state.set_state(ConversionState.base_currency)

@router.callback_query(F.data.in_({c.value for c in Currency}))
async def handle_base_currency_callback(callback: CallbackQuery, state: FSMContext):
    base = callback.data
    await state.update_data(base=base)
    await callback.answer()

    await callback.message.edit_text(
        f"✅ Base currency selected: {Currency(base).display_name}\n"
        f"Now choose the target currency:",
        reply_markup=kb.target_button
    )
    await state.set_state(ConversionState.target_currency)

@router.message(ConversionState.base_currency)
async def handle_base_currency_manual(message: Message, state: FSMContext):
    base = message.text.upper()
    if base not in {c.value for c in Currency}:
        await message.answer("❌ Invalid currency code. Try again (e.g., USD, EUR).")
        return

    await state.update_data(base=base)
    await message.answer(
        f"✅ Base currency selected: {Currency(base).display_name}\n"
        f"Now enter the target currency:"
    )
    await state.set_state(ConversionState.target_currency)

@router.callback_query(F.data.in_({f"{c.value}_2" for c in Currency}))
async def handle_target_currency_callback(callback: CallbackQuery, state: FSMContext):
    target = callback.data.replace("_2", "")
    data = await state.get_data()
    base = data.get("base")

    if base == target:
        await callback.answer()
        await callback.message.edit_text("⚠️ Base and target currencies must be different. Please choose again.")
        return

    await state.update_data(target=target)
    await callback.answer()

    await callback.message.edit_text(
        f"🎯 Target currency selected: {Currency(target).display_name}\n"
        f"Please enter the amount to convert:"
    )
    await state.set_state(ConversionState.amount_input)

@router.message(ConversionState.target_currency)
async def handle_target_currency_manual(message: Message, state: FSMContext):
    target = message.text.upper()
    if target not in {c.value for c in Currency}:
        await message.answer("❌ Invalid currency code. Try again (e.g., USD, EUR).")
        return

    data = await state.get_data()
    base = data.get("base")
    if base == target:
        await message.answer("⚠️ Base and target currencies must be different. Try again.")
        return

    await state.update_data(target=target)
    await message.answer(
        f"🎯 Target currency selected: {Currency(target).display_name}\n"
        f"Please enter the amount to convert:"
    )
    await state.set_state(ConversionState.amount_input)

@router.message(ConversionState.amount_input, F.text)
async def handle_amount_input(message: Message, state: FSMContext):
    data = await state.get_data()
    base = data.get("base")
    target = data.get("target")

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError

        rate = await get_exchange_rate(base, target)
        if rate is None:
            await message.answer("⚠️ Failed to fetch exchange rate. Please try again later.")
        else:
            result = convert_currency(amount, rate)
            await message.answer(f"💱 {amount} {base} = {result} {target}")

    except ValueError:
        await message.answer("❌ Please enter a valid positive number.")
    except Exception as e:
        logger.exception("Unexpected error during conversion")
        await message.answer("🚨 An unexpected error occurred. Please try again.")

    await state.clear()