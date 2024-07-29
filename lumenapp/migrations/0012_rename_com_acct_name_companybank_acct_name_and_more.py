# Generated by Django 5.0.2 on 2024-07-26 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lumenapp', '0011_alter_subscription_house'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companybank',
            old_name='com_acct_name',
            new_name='acct_name',
        ),
        migrations.RemoveField(
            model_name='companybank',
            name='com_acct_num',
        ),
        migrations.AddField(
            model_name='companybank',
            name='acct_num',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Account number must be between 10 and 20 digits.', regex='^\\d{10,20}$')]),
        ),
    ]