from django.core.management.base import BaseCommand, CommandError
from telegram.main import kick_by_timeout
import asyncio

class Command(BaseCommand):
    help = 'Check and send new vacancies'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        asyncio.run(kick_by_timeout())


