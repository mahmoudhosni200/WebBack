# Generated by Django 5.2.1 on 2025-05-16 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0003_remove_member_membership_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='phone_number',
        ),
    ]
