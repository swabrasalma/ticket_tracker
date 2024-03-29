# Generated by Django 2.2.3 on 2019-07-15 08:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_performedaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='phone_number',
            new_name='company_to_train',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='requestor_name',
            new_name='product_to_be_trained',
        ),
        migrations.RemoveField(
            model_name='request',
            name='amount_paid_by_customer',
        ),
        migrations.RemoveField(
            model_name='request',
            name='attachments',
        ),
        migrations.RemoveField(
            model_name='request',
            name='payment_details',
        ),
        migrations.RemoveField(
            model_name='request',
            name='qc_admin_comments',
        ),
        migrations.RemoveField(
            model_name='request',
            name='submission_comments',
        ),
        migrations.AddField(
            model_name='request',
            name='number_of_people_to_train',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='request',
            name='training_date_and_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
