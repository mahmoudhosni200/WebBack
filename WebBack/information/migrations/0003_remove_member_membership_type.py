# Generated by Django 5.2.1 on 2025-05-15 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0002_member_groups_member_is_active_member_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='membership_type',
        ),
    ]
