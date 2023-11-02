from django.conf import settings
from django.core.management.base import BaseCommand


import logging
logger = logging.getLogger(__name__)

def IngestCSV():
    pass

# turn this into a management command.
class Command(BaseCommand):
    help = "Ingests all CSV and transactions"

    def handle(self, *args, **options):
        logger.info('Ingest CSV')
        IngestCSV
        logger.info('done')