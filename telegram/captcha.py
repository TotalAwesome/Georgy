###############################################
#           Модуль капча
###############################################

import json
from random import choice
from time import time
from asgiref.sync import sync_to_async

from logging import Logger as logger
# from loguru import logger
from captcha.models import Question, Probationer
from aiogram.types import User
from telegram.local_config import ANSWER_TIMEOUT

@sync_to_async
def get_captcha_question() -> dict:
    questions = Question.objects.all()
    question = choice(questions).question_dict
    return question

@sync_to_async
def make_new_probationer(user: User, answers: list) -> None:
    obj = Probationer.objects.filter(user_id=user.id)
    if obj: 
        obj = obj.filter(actual=True)
    if obj: 
        return
    params = {
        'user_name': user.mention,
        'user_id': user.id,
        'end_time': int(time()) + ANSWER_TIMEOUT,
        'answers': json.dumps(answers, ensure_ascii=False),
        'success': None,
        'actual': True
    }
    Probationer(**params).save()
    logger.info('Испытуемый создан')
    return True

@sync_to_async
def get_answers(user: User) -> list:
    result = None
    user_id = user.id
    obj = Probationer.objects.filter(user_id=user_id)
    if obj:
        obj = obj.filter(actual=True)
        if obj:
            raw_answers = json.loads(obj[0].answers)
            result = [i.lower() for i in raw_answers]
    return result

@sync_to_async
def deactualize_probationer(user_id: int, success: None):
    obj = Probationer.objects.filter(user_id=user_id)
    if obj:
        obj = obj.filter(actual=True)
    if not obj:
        return
    obj[0].actual = False
    obj[0].success = success
    obj[0].save()

@sync_to_async
def get_timed_out_probationers():
    now = int(time())
    objects = Probationer.objects.filter(actual=True)
    if objects:
        timed_out_objects = objects.filter(end_time__lte=now)
        if timed_out_objects:
            return timed_out_objects
            # 1668290247