# Generated by Django 4.2.5 on 2023-11-09 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='orderitem',
            index=models.Index(fields=['id'], name='store_order_id_f1087c_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id'], name='store_produ_id_ecf429_idx'),
        ),
    ]
