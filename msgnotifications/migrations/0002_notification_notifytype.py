# Generated by Django 3.2 on 2021-05-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgnotifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notifyType',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
