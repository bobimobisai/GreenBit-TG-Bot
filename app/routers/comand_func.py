from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from keybords.kb import menu, language
from aiogram import types
from db import read_data
from aiogram.fsm.state import State, StatesGroup

start_photo = FSInputFile("app/images/image1.jpg")
settings_img_2 = types.InputMediaPhoto(media=start_photo)
auth_user_menu = FSInputFile("app/images/auth_user.jpg")


text_lang = "🌿GreenBit welcomes you👋!\nChoose language!"
text_en_st = "🌿GreenBit welcomes you👋!"
text_ru_st = "🌿GreenBit приветствует вас👋!"


class User(StatesGroup):
    user_id = State()
    auth_status = State()
    user_language = State()
    user_sub = State()


class UserData:
    def __init__(self, state: FSMContext):
        self.state = state

    async def get_data_fsm(self) -> dict | None:
        user_data = await self.state.get_data()

        user_id = user_data.get("user_id")
        user_auth_status = user_data.get("auth_status")
        user_language = user_data.get("user_language")
        user_sub = user_data.get("user_sub")

        user_data_fsm = {
            "user_id": user_id,
            "auth_status": user_auth_status,
            "user_language": user_language,
            "user_sub": user_sub,
        }
        if (
            user_data_fsm["user_id"] is None
            and user_data_fsm["auth_status"] is None
            and user_data_fsm["user_language"] is None
            and user_data_fsm["user_sub"] is None
        ):
            return None
        else:
            return user_data_fsm

    async def get_data_db(self, user_id: int) -> list | None:
        user_data_db = await read_data((user_id,))
        if user_data_db == []:
            return None
        else:
            return user_data_db

    async def set_user_data_fsm(
        self, user_id: int, user_lang: str, auth_status: int = 0, user_sub: int = 0
    ):
        await self.state.update_data(
            {
                "user_id": user_id,
                "auth_status": auth_status,
                "user_language": user_lang,
                "user_sub": user_sub,
            }
        )
        await self.state.set_state(User.user_id)
        await self.state.set_state(User.auth_status)
        await self.state.set_state(User.user_language)
        await self.state.set_state(User.user_sub)


class StartBaseUser:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def get_start(self, message: Message, state: FSMContext):
        cl = BaseMenu(message=message, state=state)
        data = await cl.check_data()
        # await cl.get_menu(user_lang=data["user_language"])
        if data is None:
            await message.answer_photo(
                photo=start_photo,
                caption=text_lang,
                reply_markup=language(lang="en", size=2),
            )
        else:
            await cl.get_menu(
                user_lang=data["user_language"], auth_status=data["auth_status"]
            )


class BaseMenu:
    def __init__(self, state: FSMContext, message: Message):
        self.state = state
        self.message = message

    async def check_data(self):
        data_fsm = await UserData(self.state).get_data_fsm()
        if data_fsm is not None:
            return data_fsm
        else:
            data_db = await UserData(self.state).get_data_db(
                user_id=self.message.from_user.id
            )
            if data_db is not None:
                data_db_dct = {
                    "user_id": data_db[0][0],
                    "auth_status": 1,
                    "user_language": data_db[0][6],
                    "user_sub": data_db[0][3],
                }
                await UserData(state=self.state).set_user_data_fsm(
                    user_id=data_db[0][0],
                    user_lang=data_db[0][6],
                    user_sub=data_db[0][3],
                    auth_status=1,
                )
                return data_db_dct
            else:
                return None

    async def get_menu(self, user_lang, auth_status):
        if auth_status == 1:
            if user_lang == "ru":
                await self.message.answer_photo(
                    caption=text_ru_st,
                    photo=auth_user_menu,
                    reply_markup=menu(lang="ru_user_auth", size=2),
                )
            elif user_lang == "en":
                await self.message.answer_photo(
                    caption=text_ru_st,
                    photo=auth_user_menu,
                    reply_markup=menu(lang="en_user_auth", size=2),
                )
        else:
            if user_lang == "ru":
                await self.message.answer_photo(
                    caption=text_ru_st,
                    photo=auth_user_menu,
                    reply_markup=menu(lang="ru_user_new", size=2),
                )
            elif user_lang == "en":
                await self.message.answer_photo(
                    caption=text_ru_st,
                    photo=auth_user_menu,
                    reply_markup=menu(lang="en_user_new", size=2),
                )


class Back_B:
    def __init__(self, state: FSMContext, callback: CallbackQuery):
        self.state = state
        self.callback = callback

    async def back_new(self):
        cl = BaseMenu(state=self.state, message=self.callback.message)
        data = await cl.check_data()
        if data["auth_status"] == 1:
            if data["user_language"] == "en":
                await self.callback.message.edit_media(media=settings_img_2)
                await self.callback.message.edit_caption(
                    reply_markup=menu(lang="en_user_auth")
                )
            elif data["user_language"] == "ru":
                await self.callback.message.edit_media(media=settings_img_2)
                await self.callback.message.edit_caption(
                    reply_markup=menu(lang="ru_user_auth")
                )
        else:
            if data["user_language"] == "en":
                await self.callback.message.edit_media(media=settings_img_2)
                await self.callback.message.edit_caption(
                    reply_markup=menu(lang="en_user_new")
                )
            elif data["user_language"] == "ru":
                await self.callback.message.edit_media(media=settings_img_2)
                await self.callback.message.edit_caption(
                    reply_markup=menu(lang="ru_user_new")
                )
