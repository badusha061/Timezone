# Generated by Django 4.2.3 on 2023-09-26 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=50)),
                ('coupon_code', models.CharField(max_length=50)),
                ('discount', models.PositiveIntegerField()),
                ('min_price', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField()),
            ],
        ),
    ]
