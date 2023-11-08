from django.db import models
import logging
import datetime

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
    transid = models.CharField(max_length=20,  db_index=True, unique=True)
    description = models.CharField(max_length=100, null=True)
    qty = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    symbol = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=4, null=True)

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
            logger.info("TD Ameritrade type")
            r.type = "TD"
            r.save()

    logger.info("Processing into transactions")
    for r in Rawcsv.objects.filter(ingested=False).exclude(type="UN"):
        
        if r.type=="TD":
            processTDcsv(r.csvfile)
            r.ingested = True
            r.save()

        if r.type =="SC":
            r.ingested = True
            r.save()

def processTDcsv(csvtext):
    # take the input string and process it into the rawtransaction model
    # HEADINGS LOOK LIKE THIS
    # DATE,TRANSACTION ID,DESCRIPTION,QUANTITY,SYMBOL,PRICE,COMMISSION,AMOUNT,REG FEE,SHORT-TERM RDM FEE,FUND REDEMPTION FEE, DEFERRED SALES CHARGE
    # 10/31/2023,56568972652,Sold 3 EQT Dec 15 2023 45.0 Call @ 1.13,3,EQT Dec 15 2023 45.0 Call,1.13,1.95,337.01,0.04,,,
    logger.info("Processing TD Ameritrade file")    

    for line in csvtext.split("\n"):
        if "DATE,TRANSACTION ID" in line or "***END" in line or len(line) == 0:
            logger.info(f"skipping invalid line {line}")
            continue
        
        fields = line.split(",")
        logger.info(fields)

        datestr = datetime.datetime.strptime(fields[0], "%m/%d/%Y").date()

        # attempt to create a new transaction / date record
        obj, created = Rawtransactions.objects.get_or_create(
            date = datestr,
            transid = fields[1]
        )

        if not created:
            logger.info("Skipping duplicate transaction")
            continue

        if created:
            obj.description = fields[2]
            obj.qty = 0 if fields[3]=="" else fields[3]
            obj.symbol = fields[4]
            obj.price = 0 if fields[5]=="" else fields[5]
            obj.amount = 0 if fields[6]=="" else fields[6]
            obj.save()
