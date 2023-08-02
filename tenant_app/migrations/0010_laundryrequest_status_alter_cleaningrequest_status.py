# Generated by Django 4.2.3 on 2023-08-02 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0009_remove_laundryrequest_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundryrequest',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Pending'), (1, 'Received'), (2, 'Washing'), (3, 'Drying'), (4, 'Ironing'), (5, 'Ready')], default=0),
        ),
        migrations.AlterField(
            model_name='cleaningrequest',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Scheduled'), (1, 'Completed'), (2, 'Cancelled (Room Locked)')], default=0),
        ),
    ]