# Generated by Django 4.2 on 2023-06-21 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattachment',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
