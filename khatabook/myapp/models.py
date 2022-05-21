from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=12)
    customer_of = models.ForeignKey(User,on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return '{} {} {}'.format(self.title, self.desc, self.customer_of)


class PurchaseDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name=models.CharField(max_length=100)
    total_price = models.IntegerField()
    paid_price = models.IntegerField()
    remain_price = models.IntegerField()
    customer_id = models.ForeignKey(Todo, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return '{} {} {}'.format(self.product_name, self.total_price, self.paid_price)