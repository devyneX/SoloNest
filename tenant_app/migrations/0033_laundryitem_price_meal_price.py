# Generated by Django 4.2.3 on 2023-08-15 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0032_alter_meal_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundryitem',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='meal',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
