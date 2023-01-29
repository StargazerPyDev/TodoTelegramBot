import aiogram.utils.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from base.keyboards import *
from base.states import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from base.config import TELEGRAM_API_KEY
from aiogram import Bot
import sqlite3
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


async def set_note_schedule_handler(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    state_data['schedule'] = callback_query.data
    answer = 'В какое время напомнить?'
    await SetNoteScheduleStatesGroup.set_time_state.set()
    await callback_query.message.edit_text(text=answer, reply_markup=set_schedule_time_keyboard)


async def open_folder_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    folder_id = callback_query.data.split('open_folder_')[1]
    folder = cursor.execute(f'SELECT name, created, id FROM folders WHERE id={folder_id}').fetchone()
    notes_in_folder = cursor.execute(
        f'SELECT id, created, text FROM notes WHERE folder_id={folder_id}').fetchall()

    answer = '📁 Папка "{}"\n\n' \
             '📅 Создана {}\n\n' \
             '/myfolders - ваши папки'.format(*folder)

    def _make_keyboard():
        folder_keyboard = InlineKeyboardMarkup()
        for note in notes_in_folder:
            button_text = '{} | {}'.format(note[1], note[2])
            folder_keyboard.add(InlineKeyboardButton(text=button_text,
                                                     callback_data=note[0]))
        folder_keyboard.add(InlineKeyboardButton(text='🗑 Удалить папку',
                                                 callback_data='delete_folder'))
        return folder_keyboard

    await callback_query.message.edit_text(text=answer, reply_markup=_make_keyboard())
    await FolderStatesGroup.view_folder_state.set()

    data = {
        'folder_id': folder[2]
    }
    await state.update_data(data=data)


async def delete_note_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    note_id = callback_query.data.split('delete_note_')[1]

    cursor.execute(f'DELETE FROM notes WHERE id={note_id}')
    database.commit()

    answer = '🗑 Заметка удалена'
    await callback_query.message.delete()
    await callback_query.message.answer(text=answer)


async def view_note_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    try:
        folder_id, text, photo, video, animation, voice, video_note, document, created = \
            cursor.execute(
                f'SELECT folder_id, text, photo, video, animation, voice, '
                f'video_note, document, created FROM notes WHERE id={callback_query.data}'
            ).fetchone()

        folder_name = cursor.execute(f'SELECT name FROM folders WHERE id={folder_id}').fetchone()[0]

        answer = '📖 {}\n\n' \
                 '📅 {}\n\n' \
                 '📁 {}\n\n' \
                 '/myfolders - ваши папки'.format(text, created, folder_name)

        note_keyboard = InlineKeyboardMarkup()
        note_keyboard.add(InlineKeyboardButton(text='✏ Изменить заметку',
                                               callback_data='edit_note_{}'.format(callback_query.data)))
        note_keyboard.add(InlineKeyboardButton(text='🗑 Удалить заметку',
                                               callback_data='delete_note_{}'.format(callback_query.data)))
        note_keyboard.add(InlineKeyboardButton(text='⬅ Вернуться в папку',
                                               callback_data='open_folder_{}'.format(folder_id)))

        try:
            await callback_query.message.delete()
            if photo:
                await callback_query.message.answer_photo(photo=photo, caption=answer, reply_markup=note_keyboard)
            elif video:
                await callback_query.message.answer_video(video=video, caption=answer, reply_markup=note_keyboard)
            elif animation:
                await callback_query.message.answer_animation(animation=animation, caption=answer,
                                                              reply_markup=note_keyboard)
            elif voice:
                await callback_query.message.answer_voice(voice=voice, caption=answer, reply_markup=note_keyboard)
            elif video_note:
                await callback_query.message.answer_video_note(video_note=video_note, reply_markup=note_keyboard)
            elif document:
                await callback_query.message.answer_document(document=document, caption=answer,
                                                             reply_markup=note_keyboard)
            else:
                await callback_query.message.answer(text=answer, reply_markup=note_keyboard)
        except aiogram.utils.exceptions.BadRequest:
            answer = '❗ Ошибка загрузки заметки'
            await callback_query.message.answer(text=answer, reply_markup=note_keyboard)
    except TypeError:
        state_data = await state.get_data()
        folder_id = state_data.get('folder_id')

        notes_in_folder = cursor.execute(
            f'SELECT id, created, text FROM notes WHERE folder_id={folder_id}').fetchall()

        def _make_keyboard():
            folder_keyboard = InlineKeyboardMarkup()
            for note in notes_in_folder:
                button_text = '{} | {}'.format(note[1], note[2])
                folder_keyboard.add(InlineKeyboardButton(text=button_text,
                                                         callback_data=note[0]))
            folder_keyboard.add(InlineKeyboardButton(text='🗑 Удалить папку',
                                                     callback_data='delete_folder'))
            return folder_keyboard

        await callback_query.message.edit_reply_markup(reply_markup=_make_keyboard())


async def edit_note_cq_handler(callback_query: CallbackQuery, state: FSMContext):
    note_id = callback_query.data.split('edit_note_')[1]

    await NoteStatesGroup.edit_note_state.set()
    data = {'note_id': note_id}
    await state.update_data(data=data)

    await callback_query.message.delete()
    answer = '📖 Отправьте новую заметку в чат'
    await callback_query.message.answer(text=answer, reply_markup=cancel_keyboard)


async def delete_folder_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    state_data = await state.get_data()
    folder_id = state_data.get('folder_id', None)
    notes_in_folder = cursor.execute(
        f'SELECT id, created, text FROM notes WHERE folder_id={folder_id}').fetchall()

    if not notes_in_folder:
        if folder_id:
            cursor.execute(f'DELETE FROM folders WHERE id={folder_id}')
            database.commit()
            answer = '✅ Папка удалена\n\n' \
                     '/myfolders - ваши папки'
        else:
            answer = '❗ Ошибка удаления папки'
        await callback_query.message.edit_text(text=answer)
    else:
        answer = '❗ В папке не должно быть заметок'
        await callback_query.answer(text=answer)


async def select_note_folder_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    state_data = await state.get_data()

    cursor.execute(f'INSERT INTO notes (creator, folder_id, text, photo, '
                   f'video, animation, voice, video_note, document, created) VALUES ('
                   f'{callback_query.from_user.id}, {callback_query.data}, '
                   f'{state_data.get("text", None)}, '
                   f'{state_data.get("photo", None)}, '
                   f'{state_data.get("video", None)}, '
                   f'{state_data.get("animation", None)}, '
                   f'{state_data.get("voice", None)}, '
                   f'{state_data.get("video_note", None)}, '
                   f'{state_data.get("document", None)},'
                   f'"{get_current_date()}");')
    database.commit()

    folder = cursor.execute(f'SELECT name FROM folders WHERE id={callback_query.data}').fetchone()

    answer = f'✏ Заметка сохранена в папку "{folder[0]}"\n\n' \
             f'/myfolders - ваши папки'
    await callback_query.message.edit_text(text=answer)


async def create_new_folder_cq_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    answer = '📁 Отправь название новой папки'
    await callback_query.message.edit_text(text=answer, reply_markup=cancel_keyboard)

    await FolderStatesGroup.set_new_folder_name_state.set()
