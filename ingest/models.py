from django.db import models

# Create your models here.
class Rawcsv(models.Model):
    CSV_TYPE = [
        ("SC", "Schwab"),
        ("TD", "TD Ameritrade"),
    ]

    name = models.CharField(max_length=30, blank=True)
    csvfile = models.TextField()
    ingested = models.BooleanField()
    type = models.CharField(
        max_length=2,
        choices=CSV_TYPE, 
        default="TD",
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
