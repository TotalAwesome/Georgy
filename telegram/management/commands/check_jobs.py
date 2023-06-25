from django.core.management.base import BaseCommand, CommandError
from telegram.hh import JobHhunter
from telegram.main import check_new_jobs
import asyncio

class Command(BaseCommand):
    help = 'Check and send new vacancies'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        jh = JobHhunter()
        jh.check_new_vacancies()
        asyncio.run(check_new_jobs())


