# Generated by Django 3.2 on 2021-05-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20210506_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
