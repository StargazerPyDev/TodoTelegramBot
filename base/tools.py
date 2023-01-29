import random
from string import ascii_lowercase, ascii_uppercase

import asyncio


# from aiogram import Bot
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# import asyncio
# import sqlite3


def get_absolute_value(execute_result):
    if execute_result:
        if execute_result[0]:
            return execute_result[0]
    return False


def generate_message_key():
    letters = ascii_lowercase + ascii_uppercase
    numbers = ''.join(map(str, range(10)))
    symbols = letters + numbers
    return ''.join([random.choice(symbols) for _ in range(40)])


def generate_referral_link_key():
    letters = ascii_lowercase + ascii_uppercase
    numbers = ''.join(map(str, range(10)))
    symbols = letters + numbers
    return ''.join([random.choice(symbols) for _ in range(10)])
