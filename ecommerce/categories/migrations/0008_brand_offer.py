# Generated by Django 4.2.3 on 2023-10-02 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0002_remove_offer_product_offer_offer_name'),
        ('categories', '0007_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.offer'),
        ),
    ]
