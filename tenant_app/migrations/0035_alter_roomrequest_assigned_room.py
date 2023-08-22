# Generated by Django 4.2.3 on 2023-08-20 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0034_rename_friday_mealmonthlymenu_thu_lunch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomrequest',
            name='assigned_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_requests', related_query_name='room_request', to='tenant_app.room'),
        ),
    ]