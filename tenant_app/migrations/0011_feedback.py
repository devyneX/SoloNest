# Generated by Django 4.2.2 on 2023-08-09 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0010_laundryrequest_status_alter_cleaningrequest_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.SmallIntegerField(choices=[(0, 'Meal'), (1, 'Cleaning'), (2, 'Repair'), (3, 'Laundry')])),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant_app.tenant')),
            ],
        ),
    ]