# Generated by Django 5.0.2 on 2024-07-27 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lumenapp', '0012_rename_com_acct_name_companybank_acct_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_categories',
        ),
        migrations.AddField(
            model_name='user',
            name='user_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_category', to='lumenapp.usercategory'),
        ),
    ]