# Generated by Django 2.2 on 2019-04-17 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190415_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='readed_num',
            field=models.IntegerField(default=0, verbose_name='阅读量'),
        ),
    ]