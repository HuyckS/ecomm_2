# Generated by Django 2.2.4 on 2021-09-14 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0002_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='user_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]