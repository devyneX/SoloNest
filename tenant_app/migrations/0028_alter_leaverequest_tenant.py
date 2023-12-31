# Generated by Django 4.2.3 on 2023-08-15 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0027_alter_roomrequest_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='tenant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', related_query_name='leave_request', to='tenant_app.tenant'),
        ),
    ]
