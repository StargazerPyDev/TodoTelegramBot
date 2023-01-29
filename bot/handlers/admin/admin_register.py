from bot.handlers.admin.admin_cq_handlers import *
from bot.handlers.admin.admin_msg_handlers import *
from base.filters import *

dispatcher.register_message_handler(start_handler,
                                    commands=['start'],
                                    state='*')

dispatcher.register_message_handler(help_handler,
                                    commands=['help'],
                                    state='*')

dispatcher.register_message_handler(execute_handler, CheckAdminFilter(),
                                    commands=['execute'],
                                    state='*')

dispatcher.register_message_handler(get_id, CheckProfileBlockedFilter(),
                                    commands=['id'],
                                    state='*')

dispatcher.register_message_handler(admin_dashboard, CheckAdminFilter(),
                                    commands=['admin'],
                                    state='*')

dispatcher.register_message_handler(set_mailing_text, CheckAdminFilter(),
                                    state=MailingStatesGroup.set_mailing_text_state,
                                    content_types=['text', 'photo', 'voice', 'animation'])

dispatcher.register_message_handler(select_users_count_sample, CheckAdminFilter(),
                                    state=MailingStatesGroup.select_users_count_sample_state)

dispatcher.register_message_handler(select_mailing_age_sample, CheckAdminFilter(),
                                    state=MailingStatesGroup.select_age_sample_state)

dispatcher.register_message_handler(set_mailing_keyboard, CheckAdminFilter(),
                                    state=MailingStatesGroup.set_mailing_keyboard_state)

dispatcher.register_message_handler(set_ad_text, CheckAdminFilter(),
                                    state=CustomizeAdStatesGroup.set_ad_text)

dispatcher.register_message_handler(set_welcome_message_text, CheckAdminFilter(),
                                    state=AddWelcomeMessageReferralLinkStatesGroup.set_welcome_message_text_state,
                                    content_types=['text', 'voice', 'photo', 'animation'])

dispatcher.register_message_handler(set_referral_link_name, CheckAdminFilter(),
                                    state=CreateReferralLinkStatesGroup.set_referral_link_name)

dispatcher.register_message_handler(set_ad_limit, CheckAdminFilter(),
                                    state=CustomizeAdStatesGroup.set_ad_limit)

dispatcher.register_message_handler(ban_user, CheckAdminFilter(),
                                    commands=['ban'],
                                    state='*')

dispatcher.register_message_handler(unban_user, CheckAdminFilter(),
                                    commands=['unban'],
                                    state='*')

dispatcher.register_callback_query_handler(cq_admin_dashboard, CheckAdminFilter(),
                                           lambda x: x.data == 'admin_dashboard',
                                           state='*')

dispatcher.register_callback_query_handler(create_referral_link_cq, CheckAdminFilter(),
                                           lambda x: x.data == 'create_referral_link',
                                           state='*')

dispatcher.register_callback_query_handler(view_referral_link, CheckAdminFilter(),
                                           state=ViewReferralLinksStatesGroup.open_link)

dispatcher.register_callback_query_handler(delete_referral_link, CheckAdminFilter(),
                                           lambda x: 'delete_referral_link' in x.data,
                                           state=ViewReferralLinksStatesGroup.view_link)

dispatcher.register_callback_query_handler(add_welcome_message_referral_link, CheckAdminFilter(),
                                           lambda x: 'add_welcome_message_referral_link' in x.data,
                                           state=ViewReferralLinksStatesGroup.view_link)

dispatcher.register_callback_query_handler(referral_links, CheckAdminFilter(),
                                           lambda x: x.data == 'referral_links',
                                           state='*')

dispatcher.register_callback_query_handler(set_ad_text_cq, CheckAdminFilter(),
                                           lambda x: x.data == 'ad_text')

dispatcher.register_callback_query_handler(set_ad_limit_cq, CheckAdminFilter(),
                                           lambda x: x.data == 'ad_limit')

dispatcher.register_callback_query_handler(set_ad_unique_cq, CheckAdminFilter(),
                                           lambda x: x.data == 'ad_unique')

dispatcher.register_callback_query_handler(users_statistic, CheckAdminFilter(),
                                           lambda x: x.data == 'users_statistic')

dispatcher.register_callback_query_handler(test_mailing, CheckAdminFilter(),
                                           lambda x: x.data == 'test_mailing',
                                           state='*')

dispatcher.register_callback_query_handler(set_mailing_sample_menu, CheckAdminFilter(),
                                           lambda x: x.data == 'set_mailing_sample',
                                           state='*')

dispatcher.register_callback_query_handler(customize_ad, CheckAdminFilter(),
                                           lambda x: x.data == 'customize_ad',
                                           state='*')

dispatcher.register_callback_query_handler(set_mailing_sample, CheckAdminFilter(),
                                           state=MailingStatesGroup.set_mailing_sample_state)

dispatcher.register_callback_query_handler(set_mailing_keyboard_cq, CheckAdminFilter(),
                                           lambda x: x.data == 'add_buttons',
                                           state=MailingStatesGroup.set_mailing_text_state)

dispatcher.register_callback_query_handler(mailing_dashboard_cq_handler, CheckAdminFilter(),
                                           lambda x: x.data == 'create_mailing',
                                           state='*')
