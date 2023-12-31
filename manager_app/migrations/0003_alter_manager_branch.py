# Generated by Django 4.2.3 on 2023-08-13 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0015_alter_feedback_created_at_and_more'),
        ('manager_app', '0002_alter_manager_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manager', related_query_name='manager', to='tenant_app.branch'),
        ),
    ]
