# Generated by Django 4.2.3 on 2023-08-03 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]