from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hashlib import md5
import time
import pytz

from georgy_v2.settings import TIME_ZONE

def format_date(date: datetime):
    tz = pytz.timezone(TIME_ZONE)
    date = tz.normalize(date.astimezone(tz))
    return date.strftime('%Y.%m.%d %H:%M')

def make_new_jobs_message(queryset):
    msg = 'Кому работу?\n\n'
    jobs_lines = []
    for job in queryset:
        special = ''
        currency = job.currency or ''
        if job.salary_from and job.salary_from > 100_000:
            special = '👀 '

        if job.salary_to and job.salary_from:
            salary = f'{special}от <b>{job.salary_from}</b> до <b>{job.salary_to} {currency}</b>'
        elif job.salary_from:
            salary = f'{special}<b>{job.salary_from} {currency}</b>'  
        else:
            salary = 'Наверное много :)'

        job_line = f'<a href="{job.url}">{job.name}</a>\n<i>{job.employer_name}</i>\n{salary}\n'
        jobs_lines.append(job_line)
    msg += f'<code>{"- "* 10 }</code>\n'.join(jobs_lines)
    return msg

def make_new_techworks_message(queryset):
    lines = ['👀\n']
    for tw in queryset:
        lines.append(f'<b>{tw.title}</b>\n\n<i>с {format_date(tw.start_time)} до {format_date(tw.end_time)}\n{tw.description}</i>\n')
    msg = f'{"-  "* 20}\n'.join(lines)
    return msg

def make_question_message(text):
    msg = f'<i>Добро пожаловать.\nОтветьте на простой вопрос:</i>\n<b>{text}</b>\nУ вас есть 3 минуты'
    return msg

def get_keyboard(variants: list) -> tuple:
    buttons = []
    answers = []
    for i in range(0, len(variants), 2):
        line = []
        for item in variants[i: i+2]:
            variant = item['value']
            callback = variant + str(int(time.time()))
            callback = md5(callback.encode()).hexdigest()
            line.append(InlineKeyboardButton(variant, callback_data=callback))
            if item['is_true']:
                answers.extend([variant, callback])
        buttons.append(line)
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)
    return keyboard, answers