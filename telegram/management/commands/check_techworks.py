from django.core.management.base import BaseCommand, CommandError
from telegram.maintenance import TechWorks
from telegram.main import check_new_techworks
import asyncio


class Command(BaseCommand):
    help = 'Check and send new techworks'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        tw = TechWorks()
        tw.iks_maintenance()
        asyncio.run(check_new_techworks())



