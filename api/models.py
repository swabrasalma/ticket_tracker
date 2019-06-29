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
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'requests'


class RequestComment(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    comment = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'request_comments'


class PerformedAction(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    affected_request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    performed_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    action = models.CharField(max_length = 10)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'performed_actions'


class EditLog(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    affected_column = models.CharField(max_length = 200, null=True)
    affected_request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    old_value = models.CharField(max_length=200, null=True)
    new_value = models.CharField(max_length=200, null=True)
    description = models.TextField()
    edit_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'edit_logs'


