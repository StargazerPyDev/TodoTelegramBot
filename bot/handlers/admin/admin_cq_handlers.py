import time

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from base.keyboards import *
from base.states import *
from base.tools import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from base.config import (COMPLAINS_COUNT, CUSTOMIZE_AD_INTERVAL, COMPLAINS_PEER_ID, ADMIN_IDS, TELEGRAM_API_KEY,
                         CATEGORIES)

from aiogram import Bot
import sqlite3
import asyncio
import datetime

bot = Bot(token=TELEGRAM_API_KEY)
dispatcher = Dispatcher(bot=bot,
                        storage=MemoryStorage())

database = sqlite3.connect('database.db')
cursor = database.cursor()


def get_current_date() -> str:
    """ Return today date """
    return datetime.date.today().__str__()


def get_current_date_class() -> datetime.date:
    return datetime.date.today()


def make_ad_settings():
    ad = cursor.execute(f'SELECT * FROM ad').fetchall()
    if not ad:
        cursor.execute(f'INSERT INTO ad (text) VALUES ("Показ без текста");')
        database.commit()
        ad = cursor.execute(f'SELECT * FROM ad').fetchall()[-1]
    else:
        ad = ad[-1]

    def _generate_ad_settings_message(_ad: tuple) -> str:
        if _ad:
            is_unique = 'Уникальный' if _ad[3] == 1 else 'Не уникальный'
            _answer = (f'👀 Просмотров на текущем показе: {_ad[1]}\n'
                       f'📖 Текст показа: {_ad[2]}\n\n'
                       f'❓ {is_unique}\n'
                       f'📈 Лимит показа: {_ad[4]}\n\n'
                       f'Если показ уникальный, то лимит показа - '
                       f'это лимит на человека. Если же нет, то '
                       f'лимит показа - лимит на общее кол-во показов')
            return _answer
        else:
            return '❗ Показы не настроены'

    answer = f'📊 Настойка показов;\n\n{_generate_ad_settings_message(ad)}'

    return answer


def check_ad_view(user_id) -> tuple | bool:
    ad = cursor.execute(f'SELECT * FROM ad').fetchall()
    if ad:
        ad = ad[-1]
        ad_id = ad[0]
        ad_views = ad[1]
        ad_unique = ad[3]
        ad_limit = ad[4]

        messages_count = \
            cursor.execute(f'SELECT text_messages_count FROM user_statistics WHERE user_id={user_id}').fetchone()[0]
        unique_ad_views = cursor.execute(f'SELECT COUNT(*) FROM ad_views '
                                         f'WHERE user_id={user_id} AND ad_id={ad_id}').fetchone()[0]

        if messages_count % CUSTOMIZE_AD_INTERVAL == 0 and messages_count > 0:
            if (ad_unique == 1 and unique_ad_views <= ad_limit) or \
                    (ad_unique == 0 and ad_views < ad_limit):
                if ad_unique == 1:
                    cursor.execute(f'INSERT INTO ad_views (user_id, ad_id) VALUES ('
                                   f'{user_id}, {ad_id});')
                cursor.execute(f'UPDATE ad SET views_count=views_count+1')
                return ad
    return False


async def cancel(cq: CallbackQuery, state: FSMContext):
    await cq.answer()
    await state.finish()

    answer = '✅ Действие отменено'
    await cq.message.edit_text(text=answer)


async def mailing_dashboard_cq_handler(cq: CallbackQuery, state: FSMContext):
    await cq.answer()
    await MailingStatesGroup.set_mailing_text_state.set()

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('⬅ Назад', callback_data='admin_dashboard'))

    answer = ('⌛ Отправь текст рассылки.\n\n'
              'Если хочешь, чтобы к рассылке добавились '
              'фотографии - прикрепи и их.\n'
              'Поддержка html встроена.\n\n')
    await cq.message.edit_text(text=answer,
                               reply_markup=keyboard)


async def set_mailing_keyboard_cq(cq: CallbackQuery, state: FSMContext):
    await cq.answer()
    await MailingStatesGroup.set_mailing_keyboard_state.set()

    answer = ('📌 Чтобы добавить кнопки, напиши '
              'их в следующем формате:\n\n'
              'текст - ссылка\n'
              'текст1 - ссылка1.\n\n'
              'Пример:\nНажми! - https://google.com\n'
              'Нажми ещё! - https://google.com')
    await cq.message.edit_text(text=answer)


async def test_mailing(cq: CallbackQuery, state: FSMContext):
    await cq.answer()
    data = await state.get_data()

    answer = ('ℹ Сейчас рассылка выглядит так:\n\n'
              '{}'.format(data['mailingText']))

    keyboard = InlineKeyboardMarkup()
    if data.get('mailingKeyboard'):
        for button in data['mailingKeyboard']:
            keyboard.add(InlineKeyboardButton(text=button, url=data['mailingKeyboard'][button]))

    photo = data.get('mailingPhoto', None)
    voice = data.get('mailingVoice', None)
    animation = data.get('mailingAnimation', None)

    if photo:
        await cq.message.answer_photo(photo=photo, caption=answer, reply_markup=keyboard, parse_mode='html')
    elif voice:
        await cq.message.answer_voice(voice=voice, caption=answer, reply_markup=keyboard, parse_mode='html')
    elif animation:
        await cq.message.answer_animation(animation=animation, caption=answer, reply_markup=keyboard, parse_mode='html')
    else:
        await cq.message.answer(text=answer, reply_markup=keyboard, parse_mode='html')


async def set_mailing_sample_menu(cq: CallbackQuery, state: FSMContext):
    await MailingStatesGroup.set_mailing_sample_state.set()
    await cq.answer()

    answer = '👥 Укажите выборку рассылки'
    await cq.message.edit_text(text=answer, reply_markup=mailing_samples_keyboard)


async def set_mailing_sample(cq: CallbackQuery, state: FSMContext):
    await cq.answer()
    if 'sample' in cq.data and ('male' in cq.data or 'all' in cq.data):
        answer = '📊 Начинаю рассылку'
        await cq.message.edit_text(text=answer)

        data = await state.get_data()
        photo = data.get('mailingPhoto', None)
        voice = data.get('mailingVoice', None)
        animation = data.get('mailingAnimation', None)
        text = data['mailingText']
        raw_keyboard = data.get('mailingKeyboard', None)

        keyboard = None
        if raw_keyboard:
            keyboard = InlineKeyboardMarkup()
            for button in raw_keyboard:
                keyboard.add(InlineKeyboardButton(text=button, url=raw_keyboard[button]))

        async def mailing():
            sample = cq.data.split('_sample')[0]
            params = str()
            if sample != 'all':
                params += f' AND sex="{sample}"'
            if data.get('ageSample'):
                try:
                    start_age, finish_age = list(map(str.strip, data.get('ageSample').split('-')))
                    params += f' AND age<={finish_age} AND age>={start_age}'
                except ValueError:
                    ...

            if data.get('usersCountSample'):
                params += f' LIMIT {data.get("usersCountSample")}'
            user_ids = cursor.execute(f'SELECT user_id FROM users WHERE is_blocked=0{params}').fetchall()

            users_count = len(user_ids)
            blocked_users_count = 0

            start = time.time()

            for user_id in user_ids:
                user_id = user_id[0]
                try:
                    if photo:
                        await bot.send_photo(chat_id=user_id,
                                             photo=photo,
                                             caption=text,
                                             parse_mode='html',
                                             reply_markup=keyboard
                                             )
                    elif voice:
                        await bot.send_voice(chat_id=user_id,
                                             voice=voice,
                                             caption=text,
                                             parse_mode='html',
                                             reply_markup=keyboard
                                             )
                    elif animation:
                        await bot.send_animation(chat_id=user_id,
                                                 animation=animation,
                                                 caption=text,
                                                 parse_mode='html',
                                                 reply_markup=keyboard
                                                 )
                    else:
                        await bot.send_message(chat_id=user_id,
                                               text=text,
                                               parse_mode='html',
                                               reply_markup=keyboard)
                    cursor.execute(f'UPDATE users SET '
                                   f'is_blocked=0 WHERE '
                                   f'user_id={user_id}')
                except Exception as error:
                    blocked_users_count += 1
                    cursor.execute(f'UPDATE users SET '
                                   f'is_blocked=1 WHERE '
                                   f'user_id={user_id}')

            await bot.send_message(chat_id=cq.from_user.id,
                                   text='📊 Статистика рассылки\n\n'
                                        f'Всего пользователей: {users_count}\n'
                                        f'Активных: {users_count - blocked_users_count}\n'
                                        f'Заблокированные: {blocked_users_count}\n\n'
                                        f'⌛ Время рассылки: {round(time.time() - start, 1)}s.')

        await cq.message.answer(text=f'✅ Рассылка запущена.')
        asyncio.create_task(mailing())
        await state.finish()

    elif cq.data == 'select_mailing_age_sample':
        answer = 'Укажите выборку возраста в следующем формате:\n' \
                 'Начальный возраст-конечный возраст.\n\n' \
                 'Пример:\n' \
                 '14-20'
        await cq.message.edit_text(text=answer)
        await MailingStatesGroup.select_age_sample_state.set()

    elif cq.data == 'select_users_count_sample':
        answer = 'Укажи количество пользователей в рассылке числом:'
        await cq.message.edit_text(text=answer)
        await MailingStatesGroup.select_users_count_sample_state.set()


async def customize_ad(cq: CallbackQuery, state: FSMContext):
    await cq.answer()

    ad = cursor.execute(f'SELECT * FROM ad').fetchall()
    if not ad:
        cursor.execute(f'INSERT INTO ad (text) VALUES ("Показ без текста");')
        database.commit()
        ad = cursor.execute(f'SELECT * FROM ad').fetchall()[-1]
    else:
        ad = ad[-1]

    def _generate_ad_settings_message(_ad: tuple) -> str:
        if _ad:
            is_unique = 'Уникальный' if _ad[3] == 1 else 'Не уникальный'
            _answer = (f'👀 Просмотров на текущем показе: {_ad[1]}\n'
                       f'📖 Текст показа: {_ad[2]}\n\n'
                       f'❓ {is_unique}\n'
                       f'📈 Лимит показа: {_ad[4]}\n\n'
                       f'Если показ уникальный, то лимит показа - '
                       f'это лимит на человека. Если же нет, то '
                       f'лимит показа - лимит на общее кол-во показов')
            return _answer
        else:
            return '❗ Показы не настроены'

    answer = f'📊 Настойка показов;\n\n{_generate_ad_settings_message(ad)}'

    await cq.message.edit_text(text=answer, parse_mode='html',
                               reply_markup=customize_ad_keyboard)


async def set_ad_text_cq(cq: CallbackQuery, state: FSMContext):
    await cq.answer()

    answer = '📖 Отправьте в чат текст показа;\nПоддержка html встроена.\n\n'

    await cq.message.edit_text(text=answer)
    await CustomizeAdStatesGroup.set_ad_text.set()


async def set_ad_limit_cq(cq: CallbackQuery, state: FSMContext):
    await cq.answer()

    await cq.message.edit_text(text='📖 Отправьте в чат лимит показов на человека;', reply_markup=cancel_keyboard)
    await CustomizeAdStatesGroup.set_ad_limit.set()


async def set_ad_unique_cq(cq: CallbackQuery, state: FSMContext):
    await cq.answer()

    ad = cursor.execute(f'SELECT * FROM ad').fetchall()[-1]
    cursor.execute(f'UPDATE ad SET is_unique={1 if ad[3] == 0 else 0};')
    database.commit()

    await cq.message.edit_text(text=make_ad_settings(), parse_mode='html',
                               reply_markup=customize_ad_keyboard)
    await state.finish()


async def users_statistic(cq: CallbackQuery, state: FSMContext):
    await cq.answer()

    def get_pers(table_column_name: str):
        per_all_time = cursor.execute(f'SELECT COUNT(*) '
                                      f'FROM {table_column_name}').fetchone()[0]
        per_day = cursor.execute(f'SELECT COUNT(*) '
                                 f'FROM {table_column_name} WHERE '
                                 f'created='
                                 f'"{get_current_date()}"').fetchone()[0]
        per_month = 0
        per_week = 0

        for index in range(31):
            days_invetral = datetime.timedelta(days=index)
            interval = get_current_date_class() - days_invetral
            format_interval = str(interval)
            if index <= 7:
                per_week += cursor.execute(f'SELECT COUNT(*) '
                                           f'FROM {table_column_name} WHERE '
                                           f'created='
                                           f'"{format_interval}"').fetchone()[0]
            per_month += cursor.execute(f'SELECT COUNT(*) '
                                        f'FROM {table_column_name} WHERE '
                                        f'created='
                                        f'"{format_interval}"').fetchone()[0]
        data = {
            'per_day': per_day,
            'per_week': per_week,
            'per_month': per_month,
            'per_all_time': per_all_time
        }
        return data

    def generate_pers_answer(pers_data: dict, verbose_name_plural: str) -> str:
        _answer = (f'Всего: {pers_data["per_all_time"]} {verbose_name_plural}.\n'
                   f'За сегодня: {pers_data["per_day"]} {verbose_name_plural}.\n'
                   f'За неделю: {pers_data["per_week"]} {verbose_name_plural}.\n'
                   f'За месяц: {pers_data["per_month"]} {verbose_name_plural}.\n')
        return _answer

    users_pers = get_pers('users')
    messages_pers = get_pers('messages')

    public_messages = cursor.execute(f'SELECT COUNT(*) '
                                     f'FROM public_messages').fetchone()[0]
    messages = cursor.execute(f'SELECT COUNT(*) '
                              f'FROM messages').fetchone()[0]

    answer = ('📊 Статистика пользователей\n\n'
              f'🔔 Новые пользователи:\n{generate_pers_answer(users_pers, "чел")}\n'
              f'✉ Сообщений боту:\nВсего: {messages_pers["per_all_time"]}\n\n'
              f'👀 Публичных сообщений:\nВсего: {public_messages}\n\n'
              f'🔑 Зашифрованные сообщения:\nВсего: {messages}')
    await cq.message.edit_text(text=answer, reply_markup=admin_dashboard_keyboard)


async def create_referral_link_cq(cq: CallbackQuery, state: FSMContext):
    await cq.answer()

    answer = 'Укажи имя реферальной ссылки:'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('⬅ Назад', callback_data='referral_links'))

    await cq.message.edit_text(text=answer, reply_markup=keyboard)

    await CreateReferralLinkStatesGroup.set_referral_link_name.set()


async def referral_links(cq: CallbackQuery, state: FSMContext):
    links = cursor.execute(f'SELECT id, name FROM referral_links').fetchall()

    keyboard = InlineKeyboardMarkup()
    for link in links:
        keyboard.add(InlineKeyboardButton(text=link[1], callback_data=link[0]))
    keyboard.add(InlineKeyboardButton('➕ Создать реф. ссылку',
                                      callback_data='create_referral_link'))
    keyboard.add(InlineKeyboardButton('⬅ Назад', callback_data='admin_dashboard'))
    answer = '⛓ Выбери ссылку для просмотра:'
    await cq.message.edit_text(text=answer, reply_markup=keyboard)

    await ViewReferralLinksStatesGroup.open_link.set()


async def view_referral_link(cq: CallbackQuery, state: FSMContext):
    link = cursor.execute(f'SELECT id, name, created FROM referral_links WHERE id="{cq.data}"').fetchone()
    invited_count = \
        cursor.execute(f'SELECT COUNT(*) FROM referral_invited_users WHERE referral_link_id="{cq.data}"').fetchone()[0]

    message = cursor.execute(
        f'SELECT message FROM welcome_messages_referral_links WHERE link_id="{cq.data}"').fetchone()
    bot_me = await bot.get_me()

    answer = f'⛓ Ссылка #{link[0]}\n\n' \
             f'Ссылка: https://t.me/{bot_me["username"]}?start={link[0]}\n' \
             f'Пользователей перешло: {invited_count}\n' \
             f'Название: {link[1]}\n' \
             f'Дата создания: {link[2]}\n\n' \
             f'✉ Сообщение: {get_absolute_value(message)}'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('✉ Добавить сообщение',
                                      callback_data=f'add_welcome_message_referral_link_{link[0]}'))
    keyboard.add(InlineKeyboardButton('❌ Удалить',
                                      callback_data=f'delete_referral_link_{link[0]}'))
    keyboard.add(InlineKeyboardButton('⬅ Ссылки',
                                      callback_data='referral_links'))

    await cq.message.edit_text(text=answer, reply_markup=keyboard)

    await ViewReferralLinksStatesGroup.view_link.set()


async def delete_referral_link(cq: CallbackQuery, state: FSMContext):
    link_id = cq.data.split('delete_referral_link_')[1]
    cursor.execute(f'DELETE FROM referral_links WHERE id="{link_id}"')
    database.commit()

    answer = '✅ Ссылка удалена'

    await cq.message.edit_text(text=answer, reply_markup=admin_dashboard_keyboard)


async def add_welcome_message_referral_link(cq: CallbackQuery, state: FSMContext):
    link_id = cq.data.split('add_welcome_message_referral_link_')[1]
    cursor.execute(f'INSERT OR IGNORE INTO '
                   f'welcome_messages_referral_links '
                   f'(link_id) VALUES ("{link_id}")')
    database.commit()

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('⬅ Ссылки',
                                      callback_data='referral_links'))

    answer = '✉ Добавьте текст. Если хотите прикрепить фото, - отправьте фото с текстом.'

    await cq.message.edit_text(text=answer, reply_markup=keyboard)

    await AddWelcomeMessageReferralLinkStatesGroup.set_welcome_message_text_state.set()

    data = {'link_id': link_id}

    await state.set_data(data=data)


async def cq_admin_dashboard(cq: CallbackQuery, state: FSMContext):
    answer = ('📊 Панель '
              'администрирования.')
    await cq.message.edit_text(text=answer, reply_markup=admin_dashboard_keyboard)
    await state.finish()
