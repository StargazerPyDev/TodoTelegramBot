from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

cancel_button = InlineKeyboardButton(text='❌ Отмена',
                                     callback_data='cancel')
cancel_keyboard = InlineKeyboardMarkup().add(cancel_button)

select_sex_keyboard = InlineKeyboardMarkup()
select_sex_keyboard.add(InlineKeyboardButton(text='Мужской 😎',
                                             callback_data='male'))
select_sex_keyboard.add(InlineKeyboardButton(text='Женский 👠',
                                             callback_data='female'))

search_dialog_menu_keyboard = InlineKeyboardMarkup()
search_dialog_menu_keyboard.add(InlineKeyboardButton(text='Поиск собеседника 🔍',
                                                     callback_data='search_companion'))
# search_dialog_menu_keyboard.add(InlineKeyboardButton(text='Поиск группового чата 👥🔍',
#                                                      callback_data='search_group_chat'))
search_dialog_menu_keyboard.add(InlineKeyboardButton(text='Сменить режим чата ⚙',
                                                     callback_data='change_chat_mode'))

complain_reason_keyboard = InlineKeyboardMarkup()
complain_reason_keyboard.add(InlineKeyboardButton(text='🚫 18+',
                                                  callback_data='reason_1'))
complain_reason_keyboard.add(InlineKeyboardButton(text='🚫 Детская порнография',
                                                  callback_data='reason_2'))
complain_reason_keyboard.add(InlineKeyboardButton(text='🚫 Реклама',
                                                  callback_data='reason_3'))
complain_reason_keyboard.add(InlineKeyboardButton(text='🚫 Спам',
                                                  callback_data='reason_4'))
complain_reason_keyboard.add(InlineKeyboardButton(text='❓ Другое',
                                                  callback_data='reason_other'))

cancel_search_dialog_keyboard = InlineKeyboardMarkup()
cancel_search_dialog_keyboard.add(InlineKeyboardButton(text='Отмена ❌',
                                                       callback_data='cancel_search_dialog'))

admin_dashboard_keyboard = InlineKeyboardMarkup()
admin_dashboard_keyboard.add(InlineKeyboardButton('✉ Создать рассылку',
                                                  callback_data='create_mailing'))
admin_dashboard_keyboard.add(InlineKeyboardButton('⛓ Реф. ссылки',
                                                  callback_data='referral_links'))
admin_dashboard_keyboard.add(InlineKeyboardButton('💬 Настроить показы',
                                                  callback_data='customize_ad'))
admin_dashboard_keyboard.add(InlineKeyboardButton('📈 Статистика пользователей',
                                                  callback_data='users_statistic'))

create_mailing_set_text_keyboard = InlineKeyboardMarkup()
create_mailing_set_text_keyboard.add(InlineKeyboardButton('➡ Далее',
                                                          callback_data='set_mailing_sample'))
create_mailing_set_text_keyboard.add(InlineKeyboardButton('📊 Протестировать',
                                                          callback_data='test_mailing'))
create_mailing_set_text_keyboard.add(InlineKeyboardButton('📌 Настроить кнопки',
                                                          callback_data='add_buttons'))
create_mailing_set_text_keyboard.add(cancel_button)

set_mailing_sample_keyboard = InlineKeyboardMarkup()

set_mailing_sample_keyboard.add(InlineKeyboardButton('➡ Далее',
                                                     callback_data='set_mailing_sample'))
set_mailing_sample_keyboard.add(InlineKeyboardButton('📊 Протестировать',
                                                     callback_data='test_mailing'))
set_mailing_sample_keyboard.add(cancel_button)

mailing_samples_keyboard = InlineKeyboardMarkup()

mailing_samples_keyboard.add(InlineKeyboardButton('👥 Рассылка по всем',
                                                  callback_data='all_sample'))
mailing_samples_keyboard.add(InlineKeyboardButton('♂ Рассылка по муж.',
                                                  callback_data='male_sample'))
mailing_samples_keyboard.add(InlineKeyboardButton('♀ Рассылка по жен.',
                                                  callback_data='female_sample'))
mailing_samples_keyboard.add(InlineKeyboardButton('📅 Указать возраст',
                                                  callback_data='select_mailing_age_sample'))
mailing_samples_keyboard.add(InlineKeyboardButton('🔃 Указать кол-во человек',
                                                  callback_data='select_users_count_sample'))

customize_ad_keyboard = InlineKeyboardMarkup()
customize_ad_keyboard.add(InlineKeyboardButton(text='📖 Текст показа',
                                               callback_data='ad_text'))
customize_ad_keyboard.add(InlineKeyboardButton(text='❓ Ред. уникальность',
                                               callback_data='ad_unique'))
customize_ad_keyboard.add(InlineKeyboardButton(text='📈 Лимит на чел-а',
                                               callback_data='ad_limit'))
customize_ad_keyboard.add(InlineKeyboardButton('⬅ Назад', callback_data='admin_dashboard'))

schedules_keyboard = InlineKeyboardMarkup()
schedules_keyboard.add(InlineKeyboardButton(text='Сегодня ⏳',
                                            callback_data='today'))
schedules_keyboard.add(InlineKeyboardButton(text='Завтра ⏳',
                                            callback_data='tomorrow'))
schedules_keyboard.add(InlineKeyboardButton(text='Каждый день ⏳',
                                            callback_data='everyday'))

set_schedule_time_keyboard = InlineKeyboardMarkup()

buttons = []
for hour in range(6, 24):
    buttons.append(InlineKeyboardButton(text='{}:00 ⏰'.format(hour),
                                        callback_data='{}:00'.format(hour)))
set_schedule_time_keyboard.add(*buttons)
