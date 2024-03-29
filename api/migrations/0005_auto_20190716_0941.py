# Generated by Django 2.2.3 on 2019-07-16 06:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190715_1119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='company_to_train',
            new_name='assigned_to',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='product_to_be_trained',
            new_name='component_with_issue',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='added_by',
            new_name='logged_by',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='created_at',
            new_name='time_and_date_logged',
        ),
        migrations.RemoveField(
            model_name='request',
            name='number_of_people_to_train',
        ),
        migrations.RemoveField(
            model_name='request',
            name='training_date_and_time',
        ),
        migrations.AddField(
            model_name='request',
            name='description',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='issue_title',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='priority',
            field=models.CharField(default='high', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='project_with_issue',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
