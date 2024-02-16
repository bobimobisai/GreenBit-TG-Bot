from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import Router, F, types
from keybords.kb import menu, language
from aiogram.fsm.context import FSMContext
from routers.comand_func import UserData, StartBaseUser, BaseMenu

from routers.handler import router


start_photo = FSInputFile("app/images/image1.jpg")
auth_user_menu = FSInputFile("app/images/auth_user.jpg")


text_en_st = "🌿GreenBit welcomes you👋!"
text_ru_st = "🌿GreenBit приветствует вас👋!"


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await StartBaseUser(user_id=message.from_user.id).get_start(
        message=message, state=state
    )


@router.message(Command("menu"))
async def command_menu(message: Message, state: FSMContext):
    cl = BaseMenu(message=message, state=state)
    data = await cl.check_data()
    await cl.get_menu(user_lang=data["user_language"], auth_status=data["auth_status"])


@router.message(Command("hellp"))
async def command_help(message: Message):
    await message.answer(text="Help Menu\n-Admin link\nhttps://t.me/petran_dev")
