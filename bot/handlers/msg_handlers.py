from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from base.keyboards import *
from base.states import *
from bot.handlers.cq_handlers import (get_current_date, database, cursor, )


async def write_chat_id_to_database_handler(msg: Message):
    cursor.execute(f'INSERT OR IGNORE INTO groups (group_id, created) '
                   f'VALUES ({msg.chat.id}, "{get_current_date()}");')
    database.commit()


async def create_note_handler(message: Message, state: FSMContext):
    data = {'text': '"' + message.html_text + '"' if message.html_text else 'NULL',
            'photo': '"' + message.photo[-1].file_id + '"' if message.photo else 'NULL',
            'video': '"' + message.video.file_id + '"' if message.video else 'NULL',
            'voice': '"' + message.video.file_id + '"' if message.video else 'NULL',
            'video_note': '"' + message.video.file_id + '"' if message.video else 'NULL',
            'animation': '"' + message.animation.file_id + '"' if message.animation else 'NULL',
            'document': '"' + message.document.file_id + '"' if message.document else 'NULL'}
    await state.update_data(data=data)

    def _make_keyboard():
        """ Генерирует клавитауру для сообщения """
        folders_keyboard = InlineKeyboardMarkup()
        folders = cursor.execute(f'SELECT id, name FROM folders WHERE creator={message.from_user.id}').fetchall()

        for folder in folders:
            folders_keyboard.add(InlineKeyboardButton(text='📁 ' + folder[1],
                                                      callback_data=folder[0]))
        folders_keyboard.add(InlineKeyboardButton(text='➕ Создать папку',
                                                  callback_data='create_new_folder'))
        folders_keyboard.add(cancel_button)

        return folders_keyboard

    answer = '📁 Выбери папку для сохранения'
    await message.answer(text=answer, reply_markup=_make_keyboard())
    await FolderStatesGroup.select_note_folder_state.set()


async def edit_note_handler(message: Message, state: FSMContext):
    text = '"' + message.html_text + '"' if message.html_text else 'NULL'
    photo = '"' + message.photo[-1].file_id + '"' if message.photo else 'NULL'
    video = '"' + message.video.file_id + '"' if message.video else 'NULL'
    voice = '"' + message.video.file_id + '"' if message.video else 'NULL'
    video_note = '"' + message.video.file_id + '"' if message.video else 'NULL'
    animation = '"' + message.animation.file_id + '"' if message.animation else 'NULL'
    document = '"' + message.document.file_id + '"' if message.document else 'NULL'

    state_data = await state.get_data()
    note_id = state_data.get('note_id')

    cursor.execute(f'UPDATE notes SET text={text}, photo={photo}, video={video},'
                   f'animation={animation}, voice={voice}, video_note={video_note}, '
                   f'document={document}, is_edit=1, edited="{get_current_date()}" WHERE id={note_id}')
    database.commit()

    answer = '✏ Заметка редактирована\n\n' \
             '/myfolders - ваши папки'

    await message.answer(text=answer)
    await state.finish()


async def user_folders_handler(message: Message, state: FSMContext):
    answer = '📁 Ваши папки'

    folders_keyboard = InlineKeyboardMarkup()
    folders = cursor.execute(f'SELECT id, name FROM folders WHERE creator={message.from_user.id}').fetchall()

    for folder in folders:
        folders_keyboard.add(InlineKeyboardButton(text='📁 ' + folder[1],
                                                  callback_data='open_folder_' + str(folder[0])))
    folders_keyboard.add(InlineKeyboardButton(text='➕ Создать папку',
                                              callback_data='create_new_folder'))

    await message.answer(text=answer, reply_markup=folders_keyboard)
    await FolderStatesGroup.view_folders_state.set()


async def create_new_folder_handler(message: Message, state: FSMContext):
    answer = '📁 Отправь название новой папки'
    await message.answer(text=answer)

    await FolderStatesGroup.set_new_folder_name_state.set()


async def set_new_folder_name_handler(message: Message, state: FSMContext):
    cursor.execute(f'INSERT INTO folders (name, created, creator) '
                   f'VALUES ("{message.text}", "{get_current_date()}", {message.from_user.id});')
    database.commit()

    answer = '✅ Папка создана\n\n' \
             '/myfolders - ваши папки'

    await message.answer(text=answer)
    await state.finish()
