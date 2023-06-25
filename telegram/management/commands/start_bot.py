from django.core.management.base import BaseCommand, CommandError
from telegram.main import start_bot
import asyncio

class Command(BaseCommand):
    help = 'start bot'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        asyncio.run(start_bot())


