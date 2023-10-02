# Generated by Django 4.2.3 on 2023-09-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=True, max_length=50, null=True)),
                ('image', models.ImageField(default='No image available', upload_to='photos/name')),
                ('is_available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'name',
            },
        ),
    ]
