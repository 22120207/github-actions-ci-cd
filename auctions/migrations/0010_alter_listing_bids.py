# Generated by Django 5.1 on 2024-09-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid_infor_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bids',
            field=models.IntegerField(default=0),
        ),
    ]
