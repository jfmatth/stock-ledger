from django.conf import settings
from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger(__name__)

from ingest.models import ingestRawcsv, processRawcsv

# turn this into a management command.
class Command(BaseCommand):
    help = "Ingests all CSV and transactions"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("filename", nargs=1, type=str, help="filename to ingest")

    def handle(self, *args, **options):
        ingestRawcsv(options['filename'][0])
        processRawcsv()
