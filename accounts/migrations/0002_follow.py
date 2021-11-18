# Generated by Django 3.0.14 on 2021-11-18 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True)),
                ('that_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to', to=settings.AUTH_USER_MODEL)),
                ('this_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]