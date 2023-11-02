r.csvfile.split("\n")


r.csvfile.split("\n")[0]
>>> r.csvfile.split("\n")[0].split(",")
['DATE', 'TRANSACTION ID', 'DESCRIPTION', 'QUANTITY', 'SYMBOL', 'PRICE', 'COMMISSION', 'AMOUNT', 'REG FEE', 'SHORT-TERM RDM FEE', 'FUND REDEMPTION FEE', ' DEFERRED SALES CHARGE\r']

r.csvfile.split("\n")[1].split(",")
['12/29/2022', '47243756251', 'Sold 3 EQT Feb 3 2023 39.0 Call @ 0.65', '3', 'EQT Feb 3 2023 39.0 Call', '0.65', '1.95', '193.01', '0.04', '', '', '\r']