from bot.handlers.admin.admin_cq_handlers import *
from bot.handlers.admin.admin_msg_handlers import *
from bot.handlers.msg_handlers import *
from base.filters import *

# Подключение админки
import bot.handlers.admin.admin_register

dispatcher.register_message_handler(edit_note_handler,
                                    state=NoteStatesGroup.edit_note_state,
                                    content_types=["text", "photo", "video", "voice", "video_note", "animation",
                                                   "document"])

dispatcher.register_message_handler(create_new_folder_handler,
                                    commands=['newfolder'],
                                    state='*')

dispatcher.register_message_handler(user_folders_handler,
                                    commands=['myfolders'],
                                    state='*')

dispatcher.register_message_handler(set_new_folder_name_handler,
                                    state=FolderStatesGroup.set_new_folder_name_state)

dispatcher.register_message_handler(create_note_handler,
                                    CheckProfileBlockedFilter(),
                                    state="*",
                                    content_types=["text", "photo", "video", "voice", "video_note", "animation",
                                                   "document"])

dispatcher.register_message_handler(write_chat_id_to_database_handler,
                                    content_types=['new_chat_members'],
                                    state='*')

dispatcher.register_message_handler(backup_handler,
                                    commands=['backup'],
                                    state='*')

dispatcher.register_callback_query_handler(open_folder_handler,
                                           lambda x: 'open_folder_' in x.data,
                                           state='*')

dispatcher.register_callback_query_handler(cancel, CheckProfileBlockedFilter(),
                                           lambda x: x.data == 'cancel',
                                           state='*')

dispatcher.register_callback_query_handler(create_new_folder_cq_handler,
                                           lambda x: x.data == 'create_new_folder',
                                           state='*')

dispatcher.register_callback_query_handler(edit_note_cq_handler,
                                           lambda x: 'edit_note_' in x.data,
                                           state='*')

dispatcher.register_callback_query_handler(delete_note_handler,
                                           lambda x: 'delete_note_' in x.data,
                                           state=FolderStatesGroup.view_folder_state)

dispatcher.register_callback_query_handler(delete_folder_handler,
                                           lambda x: x.data == 'delete_folder',
                                           state=FolderStatesGroup.view_folder_state)

dispatcher.register_callback_query_handler(view_note_handler,
                                           state=FolderStatesGroup.view_folder_state)

dispatcher.register_callback_query_handler(select_note_folder_handler,
                                           state=FolderStatesGroup.select_note_folder_state)

dispatcher.register_callback_query_handler(set_note_schedule_handler,
                                           state=SetNoteScheduleStatesGroup.set_schedule_state)
