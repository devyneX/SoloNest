# Generated by Django 4.2.3 on 2023-08-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0016_payment_bookingfee'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomrequest',
            name='approval_date',
            field=models.DateField(null=True),
        ),
    ]