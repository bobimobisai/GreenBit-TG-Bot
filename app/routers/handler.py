from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from routers.comand_func import User, UserData, BaseMenu, Back_B
from keybords.kb import language, settings, Back, menu
from db import create_data, update_data, delete_data


who_by_img = types.FSInputFile("app/images/who_by.jpg")
settings_img = types.FSInputFile("app/images/settings.jpg")
settings_img_2 = types.InputMediaPhoto(media=settings_img)

router = Router()


# колбек смены языка для не зареганных
@router.callback_query(F.data == "en")
async def lang_en(callback: types.CallbackQuery, state: FSMContext):
    text_en_st = "🌿GreenBit welcomes you👋!\nTo receive tasks, click Join✅"
    await UserData(state).set_user_data_fsm(
        user_id=callback.from_user.id, user_lang="en"
    )
    await callback.answer(text="English language selected💚")
    await callback.message.edit_caption(
        caption=text_en_st,
        reply_markup=menu(lang="en_user_new"),
    )


@router.callback_query(F.data == "ru")
async def lang_ru(callback: types.CallbackQuery, state: FSMContext):
    text_ru_st = (
        "🌿GreenBit приветствует вас👋!\nДля получения заданий нажмите Присоединиться✅"
    )
    await UserData(state).set_user_data_fsm(
        user_id=callback.from_user.id, user_lang="ru"
    )
    await callback.answer(text="Русский язык выбран💚!")
    await callback.message.edit_caption(
        caption=text_ru_st, reply_markup=menu(lang="ru_user_new")
    )


# колбек смены языка для зареганных
@router.callback_query(F.data == "en_db")
async def lang_en_db(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data(user_language="en")
        await state.set_state(User.user_language)
        await update_data(
            column="user_language",
            data="'en'",
            args=(callback.from_user.id,),
        )
    except Exception as e:
        await callback.message.answer(
            text="Ooooh fuck...\nSomething's broken bup beep...\nTry later.",
        )
    else:
        await callback.answer(text="English language selected💚")
        await menu_auth_setigs(callback, state)


@router.callback_query(F.data == "ru_db")
async def lang_ru_db(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data(user_language="ru")
        await state.set_state(User.user_language)
        await update_data(
            column="user_language",
            data="'ru'",
            args=(callback.from_user.id,),
        )
    except Exception as e:
        await callback.message.answer(
            text="Что то блять сломалось:(\nПопробуйте позже",
        )
        print(e)
    else:
        await callback.answer(text="English language selected💚")
        await menu_auth_setigs(callback, state)


# колбек для кто вы
@router.callback_query(F.data == "who_you")
async def menu_new_who(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_language = user_data.get("user_language")
    try:
        if user_language == "en":
            text = """We are a crypto company <b>GreenBit</b> that aims to support environmentally disruptive lifestyles \
            💁‍Members can earn <b>GreenBit</b> for making environmentally responsible decisions and doing their part to protect the environment."""
        else:
            text = """Мы - крипто-компания <b>GreenBit</b>, которая направлена на поддержку экологически устойчивого образа жизни\
            💁‍Участники могут зарабатывать <b>GreenBit</b> за принятие экологически ответственных решений и внесение своего вклада в охрану окружающей среды."""
    finally:
        await callback.message.edit_caption(
            caption=text, parse_mode="HTML", reply_markup=Back(size=1).as_markup()
        )


# колбек для того как купить
@router.callback_query(F.data == "how_buy")
async def menu_new_how_buy(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_language = user_data.get("user_language")
    try:
        if user_language == "en":
            text_1 = "To purchase our token, you can click on the <b>Buy</b> button, which will take you to the site for purchase👨‍"
        else:
            text_1 = "Для покупки нашего токена, вы можете нажать на кнопку <b>Купить</b>, которая переведет вас на сайт для покупки👨‍"
    finally:
        await callback.message.edit_caption(
            caption=text_1, parse_mode="HTML", reply_markup=Back(size=1).as_markup()
        )


# смена языка
@router.callback_query(F.data == "s_w")
async def menu_new_s_w(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        caption="Change language", reply_markup=language(lang="en", size=2)
    )


@router.callback_query(F.data == "s_w_db")
async def menu_new_s_w_db(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        caption="Change language", reply_markup=language(lang="en_db", size=2)
    )


# регистрация в БД и FSM
@router.callback_query(F.data == "join")
async def join_new_user(callback: types.CallbackQuery, state: FSMContext):
    text_en = "Now you are with us💚!\nTEXT"
    text_ru = "Теперь вы с нами💚!\nTEXT"

    usr = await UserData(state).get_data_fsm()
    try:
        await create_data(data=usr["user_id"])
        await update_data(
            data=f"'{usr["user_language"]}'", column="user_language", args=usr["user_id"]
        )
    except Exception as e:
        await callback.message.answer(text="Error :(\nPlease, tyr again")
        print(f"ERROR:{e}")
    finally:
        if usr["user_language"] == "en":
            await callback.message.edit_caption(
                caption=text_en, reply_markup=menu(lang="en_user_auth")
            )
        else:
            await callback.message.edit_caption(
                caption=text_ru, reply_markup=menu(lang="ru_user_auth")
            )
        await state.update_data({"auth_status": 1, "user_sub": 0})
        await state.set_data(User.auth_status)
        await state.set_data(User.user_sub)


@router.callback_query(F.data == "setigs")
async def menu_auth_setigs(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_language = user_data.get("user_language")

    if user_language == "en":
        await callback.message.edit_media(media=settings_img_2)
        await callback.message.edit_caption(
            caption="Settigs", reply_markup=settings(lang="en_set", size=2)
        )
    else:
        await callback.message.edit_media(
            media=settings_img_2,
        )
        await callback.message.edit_caption(
            caption="Настройки", reply_markup=settings(lang="ru_set", size=2))


@router.callback_query(F.data == "sub")
async def menu_auth_sub(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="sub!")


@router.callback_query(F.data == "del")
async def dell_account(callback: types.CallbackQuery, state: FSMContext):
    try:
        await delete_data(args=(callback.from_user.id,))
        await state.clear()
    except Exception as e:
        await callback.message.answer(text="Fuck....")
        print(e)
    else:
        await callback.message.answer(text="Account has been deleted.")


@router.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery, state: FSMContext):
    cl = await Back_B(state=state, callback=callback).back_new()
