
from aiogram import Bot, Dispatcher, executor, types
from random import shuffle

import logging

from .async_orm import get_new_techworks_queryset, get_new_jobs_queryset, uncheck_new
from .captcha import get_captcha_question, make_new_probationer, get_answers, \
    deactualize_probationer, get_timed_out_probationers
from telegram.messages import make_new_jobs_message, make_new_techworks_message, \
    make_question_message, get_keyboard
from telegram.local_config import *

bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


logging.basicConfig(level=logging.DEBUG)
logger = logging.Logger(__name__)

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    # print(message)
    if message.from_user.is_bot:
        return
    for new_user in message.new_chat_members:
        if new_user.is_bot:
            continue
        question = await get_captcha_question()
        keyboard = None
        answers =  [i['value'] for i in question['variants'] if i['is_true']]
        if question['type'] == 'OFFER_OPTIONS':
            shuffle(question['variants'])
            keyboard, answers = get_keyboard(question['variants'])
        new = await make_new_probationer(new_user, answers)
        if new:
            await message.reply(make_question_message(question['text']), reply_markup=keyboard)
            logger.info(f'Вопрос: {question["text"]}')


async def check_message_for_answer(tg_object):
    answers = await get_answers(user=tg_object.from_user)
    if not answers:
        return
    good_answer = None
    if isinstance(tg_object, types.CallbackQuery):
        message = tg_object.message
        good_answer = tg_object.data in answers
        source = tg_object.data
        user_id = tg_object.from_user.id
    else:
        message = tg_object
        good_answer = message.text in answers
        source = message.text
        user_id = message.from_id
    chat_id = message.chat.id
    if good_answer:
        await message.answer('Ок')
        await deactualize_probationer(user_id, success=True)
    else:
        await message.answer('Неверно')
        try:
            await bot.kick_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                revoke_messages=True
            )
        except Exception as e:
            logger.info(e)
        await deactualize_probationer(user_id, success=False)
    logger.info(f"user: {message.from_user.mention} answer: {source}")

@dp.message_handler()
async def new_message(message: types.Message):
    await check_message_for_answer(message)

@dp.callback_query_handler()
async def process_callback_button(callback_query: types.CallbackQuery):
    await callback_query.answer('')
    await check_message_for_answer(callback_query)


async def check_new_jobs():
    new_jobs = await get_new_jobs_queryset()
    if new_jobs:
        msg = make_new_jobs_message(new_jobs)
        result = await bot.send_message(CHAT_ID, msg, disable_web_page_preview=True)
        if isinstance(result, types.Message):
            await uncheck_new(new_jobs)


async def check_new_techworks():
    new_techworks = await get_new_techworks_queryset()
    if new_techworks:
        msg = make_new_techworks_message(new_techworks)
        result = await bot.send_message(CHAT_ID, msg, disable_web_page_preview=True)
        if isinstance(result, types.Message):
            try:
                await bot.pin_chat_message(result.chat.id, result.message_id)
            except Exception as e:
                logger.info(e)
            await uncheck_new(new_techworks)

async def kick_by_timeout():
    slowpocks = await get_timed_out_probationers()
    if slowpocks:
        for i in slowpocks:
            user_name = i.user_name
            user_id = i.user_id
            try:
                await bot.kick_chat_member(CHAT_ID, user_id=user_id)
            except Exception as e:
                logger.error(e)
            await deactualize_probationer(user_id, success=None)
            await bot.send_message(CHAT_ID, f'{user_name} Не осилил капчу')

def start_bot():
    while True:
        try:
            executor.start_polling(dp)
        except Exception as e:
            logger.error(e)
