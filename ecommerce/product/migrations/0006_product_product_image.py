# Generated by Django 4.2.3 on 2023-09-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='NO image is available', null=True, upload_to='product_image'),
        ),
    ]
