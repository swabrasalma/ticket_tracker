from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=250)
    full_names = models.CharField(max_length=250)
    user_role = models.CharField(max_length=150)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'users'


class Request(models.Model):
    id = models.BigAutoField(primary_key=True)
    requestor_name = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 200)
    submission_comments = models.TextField()
    attachments = models.FileField(upload_to='requests')
    status = models.CharField(max_length=20, default='New')
    amount_paid_by_customer = models.CharField(max_length=20)
    payment_details = models.TextField()
    qc_admin_comments = models.TextField()    
    class Meta:
        db_table = 'requests'



