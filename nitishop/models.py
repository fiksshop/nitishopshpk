from django.db import models


def roundit(i):
    i = round(float(i), 2)
    return i


class Results(models.Model):
    date = models.DateField()
    cashbox = models.FloatField(max_length=40)
    withdraw = models.FloatField(max_length=40)
    remain = models.FloatField(max_length=40)
    sale = models.FloatField(max_length=40)
    profit = models.FloatField(max_length=40)
    neto = models.FloatField(max_length=40)
    expense = models.FloatField(max_length=40)

    def save(self, *args, **kwargs):
        self.cashbox = roundit(self.cashbox)
        self.withdraw = roundit(self.withdraw)
        self.remain = roundit(self.remain)
        self.sale = roundit(self.sale)
        self.profit = roundit(self.profit)
        self.neto = roundit(self.neto)
        self.expense = roundit(self.expense)
        super(Results, self).save(*args, **kwargs)


class Total(models.Model):
    budget = models.FloatField(max_length=40)
    total_sale = models.FloatField(max_length=40)
    total_profit = models.FloatField(max_length=40)
    total_neto = models.FloatField(max_length=40)
    total_expense = models.FloatField(max_length=40)

    def save(self, *args, **kwargs):
        self.budget = roundit(self.budget)
        self.total_sale = roundit(self.total_sale)
        self.total_profit = roundit(self.total_profit)
        self.total_neto = roundit(self.total_neto)
        self.total_expense = roundit(self.total_expense)
        super(Total, self).save(*args, **kwargs)


class DefValues(models.Model):
    wages = models.FloatField(max_length=40, blank=True)
    transport = models.FloatField(max_length=40, blank=True)
    electricbill = models.FloatField(max_length=40, blank=True)
    internet = models.FloatField(max_length=40, blank=True)
    water = models.FloatField(max_length=40, blank=True)
    total_exp = models.FloatField(max_length=40, blank=True)
    avg_percent = models.FloatField(max_length=5, blank=True)
    day_expense = models.FloatField(max_length=5, blank=True)

    def save(self, *args, **kwargs):
        self.wages = roundit(self.wages)
        self.transport = roundit(self.transport)
        self.electricbill = roundit(self.electricbill)
        self.internet = roundit(self.internet)
        self.water = roundit(self.water)
        self.total_exp = roundit(self.total_exp)
        self.avg_percent = roundit(self.avg_percent)
        self.day_expense = roundit(self.day_expense)
        super(DefValues, self).save(*args, **kwargs)


class Suppliers(models.Model):
    supplier_name = models.CharField(max_length=85, blank=True)
    contact_name = models.CharField(max_length=85, blank=True)
    tel_number = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return '%s' % self.supplier_name


class Storage(models.Model):
    product_name = models.CharField(max_length=150, blank=True)
    stock = models.IntegerField(blank=True)
    supp_name = models.ForeignKey(Suppliers, on_delete=models.DO_NOTHING, blank=False)
