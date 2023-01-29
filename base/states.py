from aiogram.dispatcher.filters.state import State, StatesGroup


class ViewPublicMessageStatesGroup(StatesGroup):
    view_message_state = State()


class FolderStatesGroup(StatesGroup):
    set_new_folder_name_state = State()

    select_note_folder_state = State()

    view_folders_state = State()
    view_folder_state = State()


class NoteStatesGroup(StatesGroup):
    edit_note_state = State()


class SelectPublicMessagesCategoryStatesGroup(StatesGroup):
    select_category_state = State()


class CreatePublicMessageStatesGroup(StatesGroup):
    set_message_text_state = State()


class MailingStatesGroup(StatesGroup):
    set_mailing_text_state = State()
    set_mailing_keyboard_state = State()
    set_mailing_sample_state = State()
    select_age_sample_state = State()
    select_users_count_sample_state = State()


class AddWelcomeMessageReferralLinkStatesGroup(StatesGroup):
    set_welcome_message_text_state = State()


class CustomizeAdStatesGroup(StatesGroup):
    set_ad_text = State()
    set_ad_unique = State()
    set_ad_limit = State()


class CreateReferralLinkStatesGroup(StatesGroup):
    set_referral_link_name = State()


class ViewReferralLinksStatesGroup(StatesGroup):
    open_link = State()
    view_link = State()


class SetNoteScheduleStatesGroup(StatesGroup):
    set_schedule_state = State()
    set_time_state = State()
