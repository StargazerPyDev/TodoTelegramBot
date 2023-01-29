from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from base.config import ADMIN_IDS
from bot.handlers.cq_handlers import *


class CheckAdminFilter(BoundFilter):
    key = 'check_admin'

    async def check(self, msg: Message):
        return msg.from_user.id in ADMIN_IDS


class CheckProfileBlockedFilter(BoundFilter):
    key = 'check_profile_blocked'

    async def check(self, msg: Message):
        response = cursor.execute(f'SELECT is_blocked FROM users WHERE user_id={msg.from_user.id}').fetchone()
        if response:
            is_blocked = {1: False, 0: True}[response[0]]
            return is_blocked
        return True


dispatcher.filters_factory.bind(CheckAdminFilter)
