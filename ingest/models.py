from django.db import models
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class Rawcsv(models.Model):
    CSV_TYPE = [
        ("SC", "Schwab"),
        ("TD", "TD Ameritrade"),
        ("UN", "Unknown"),
    ]

    name = models.CharField(max_length=30, blank=True)
    csvfile = models.TextField()
    ingested = models.BooleanField()
    type = models.CharField(
        max_length=2,
        choices=CSV_TYPE, 
        default="UN",
    )

    def __str__(self) -> str:
        return f'{self.name} - {self.ingested} - {self.type}'


class Rawtransactions(models.Model):
    date = models.DateField()
    transid = models.TextField(max_length=20,  db_index=True)
    description = models.TextField(max_length=100)
    qty = models.DecimalField(max_digits=20, decimal_places=4)
    symbol = models.TextField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    amount = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self) -> str:
        return f'{self.date} - {self.transid}'


def ingestRawcsv(filein):
    logger.info(f"Ingesting {filein}")

    r = Rawcsv()
    r.name = filein
    r.csvfile = open(filein,'r').read()
    r.ingested = False
    r.save()

    logger.info("Ingested.")
    
def processRawcsv():
    # find all records that have not been ingested, set the type and try to extract

    logger.info("Determine type of CSV")
    # set the type of the CSV, TD or Schwab for now
    for r in Rawcsv.objects.filter(ingested=False).filter(type="UN"):

        # TD's start with "DATE, TRANSACTION ID"
        if "DATE,TRANSACTION ID" in r.csvfile.split('\n')[0]:
            r.type = "TD"
            r.save()

    logger.info("Processing into transactions")
    for r in Rawcsv.objects.filter(ingested=False).exclude(type="UN"):e
        
        if r.type=="TD":
            processTDcsv(r.csvfile)
            r.ingested = True
            r.save()


def processTDcsv(csvtext):
    # take the input string and process it into the rawtransaction model
    # HEADINGS LOOK LIKE THIS
    # DATE,TRANSACTION ID,DESCRIPTION,QUANTITY,SYMBOL,PRICE,COMMISSION,AMOUNT,REG FEE,SHORT-TERM RDM FEE,FUND REDEMPTION FEE, DEFERRED SALES CHARGE
    
    print(csvtext)    
    
    # date = models.DateField()
    # transid = models.TextField(max_length=20,  db_index=True)
    # description = models.TextField(max_length=100)
    # qty = models.DecimalField(max_digits=20, decimal_places=4)
    # symbol = models.TextField(max_length=50)
    # price = models.DecimalField(max_digits=20, decimal_places=4)
    # amount = models.DecimalField(max_digits=20, decimal_places=4)

