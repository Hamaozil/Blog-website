# Generated by Django 5.1.4 on 2024-12-30 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_userblogs_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userblogs',
            old_name='date',
            new_name='created_at',
        ),
    ]
