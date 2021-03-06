# Generated by Django 3.2 on 2021-05-05 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0006_groupinvite'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupRequestJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouprequestjoingroup', to='groups.group')),
                ('requestFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouprequestjoinfrom', to=settings.AUTH_USER_MODEL)),
                ('requestTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouprequestjointo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
