from aiogram.utils import executor
from bot.register import dispatcher
from aiogram.types import BotCommand
import sqlite3

# create tables

database = sqlite3.connect('database.db')
cursor = database.cursor()

cursor.execute(f'CREATE TABLE IF NOT EXISTS users ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'user_id INTEGER UNIQUE,'
               f'created TEXT,'
               f'is_blocked INTEGER DEFAULT 0,'
               f'age INTEGER,'  # возраст
               f'sex TEXT,'  # пол (male/female)

               f'referral_link_id INTEGER,'
               f'blocked_start TEXT,'
               f'blocked_term INTEGER,'
               f'selected_category TEXT DEFAULT "category_random"'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS referral_links ('
               f'id TEXT,'
               f'name TEXT,'
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS referral_invited_users ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'user_id UNIQUE,'
               f'referral_link_id TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS users_settings ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'user_id INTEGER UNIQUE, '
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS user_statistics ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'user_id INTEGER UNIQUE,'
               f'score TEXT,'

               f'chats_count INTEGER DEFAULT 0,'
               f'text_messages_count INTEGER DEFAULT 0,'
               f'voice_messages_count INTEGER DEFAULT 0,'
               f'video_messages_count INTEGER DEFAULT 0,'
               f'sticker_messages_count INTEGER DEFAULT 0,'
               f'photo_messages_count INTEGER DEFAULT 0,'
               f'animation_messages_count INTEGER DEFAULT 0,'
               f'video_note_messages_count INTEGER DEFAULT 0, '
               f'document_messages_count INTEGER DEFAULT 0, '
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS messages ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'key TEXT,'

               f'message_text TEXT,'
               f'message_photo TEXT,'
               f'message_video TEXT,'
               f'message_voice TEXT,'
               f'message_video_note TEXT,'
               f'message_sticker TEXT,'

               f'from_user_id INTEGER,'
               f'from_user_username TEXT,'

               f'is_anonymous INTEGER DEFAULT 1,'
               f'created TEXT, '
               f'to_user_username TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS public_messages ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'key TEXT,'

               f'message_text TEXT,'
               f'message_photo TEXT,'
               f'message_video TEXT,'
               f'message_voice TEXT,'
               f'message_video_note TEXT,'
               f'message_sticker TEXT,'

               f'from_user_id INTEGER,'
               f'from_user_username TEXT,'

               f'is_anonymous INTEGER DEFAULT 1,'
               f'created TEXT,'
               f'views INTEGER DEFAULT 0,'
               f'category TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS chats ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'companion_user_id INTEGER DEFAULT 0,'  # первый собеседник
               f'second_companion_user_id INTEGER DEFAULT 0,'  # второй собеседник
               f'chat_type TEXT DEFAULT "text",'  # тип чата (текстовый/голосовой)
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS group_chats ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'users_in_chat TEXT,'
               f'chat_type TEXT DEFAULT "text",'
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS ad ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'views_count INTEGER DEFAULT 0,'
               f'text TEXT,'
               f'is_unique INTEGER DEFAULT 0,'
               f'views_limit INTEGER DEFAULT 10'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS ad_views ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'ad_id INTEGER,'
               f'user_id INTEGER, '
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS complains ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'user_id INTEGER,'
               f'reason TEXT,'
               f'created TEXT,'
               f'message_key INTEGER'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS welcome_messages_referral_links ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'link_id UNIQUE,'
               f'message TEXT,'
               f'photo TEXT,'
               f'voice TEXT,'
               f'animation TEXT,'
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS groups ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'group_id UNIQUE,'
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS public_messages_categories ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'message_id INTEGER,'
               f'category TEXT,'
               f'user_id INTEGER'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS folders ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'creator INTEGER,'
               f'name TEXT,'
               f'created TEXT'
               f');')

cursor.execute(f'CREATE TABLE IF NOT EXISTS notes ('
               f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               f'creator INTEGER,'
               f'folder_id INTEGER,'
               f'text TEXT,'
               f'photo TEXT,'
               f'video TEXT,'
               f'animation TEXT,'
               f'voice TEXT,'
               f'video_note TEXT,'
               f'document TEXT,'
               f'created TEXT,'
               f'is_edit INTEGER DEFAULT 0,'
               f'edited TEXT'
               f');')

database.close()


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand('start', 'Запуск бота'),
            BotCommand('newfolder', 'Создать папку'),
            BotCommand('myfolders', 'Ваши папки'),
        ]
    )


async def start(dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    await set_default_commands(dispatcher)
    print(f'#    start on @{bot_name}')


async def end(dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    print(f'#    end on @{bot_name}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher,
                           on_startup=start,
                           on_shutdown=end)
