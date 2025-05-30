from django.db import models
from django.contrib.postgres.fields import ArrayField

from crm.models import Customer
from useraccount.models import User

class VocRecord(models.Model):
    id=models.AutoField(primary_key=True, editable=False)
    user=models.ForeignKey(User, related_name='voc_records', on_delete=models.DO_NOTHING)
    customer=models.ForeignKey(Customer, related_name='voc_records', on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True, editable=False)
    summary=models.TextField(null=True)
    opinion=models.TextField(blank=True, null=True)
    keyword=ArrayField(models.TextField(), blank=True, default=[])
    context=models.TextField(null=True)

# class Record(models.Model):
#     id = models.AutoField(primary_key=True)
#     counselor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='counselor')
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
#     file = models.FileField(upload_to='uploads/record/%Y/%m/%d/', editable=False)
#     context = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True, editable=False)
