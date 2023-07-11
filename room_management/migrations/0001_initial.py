# Generated by Django 4.2.3 on 2023-07-11 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.CharField(max_length=10)),
                ('room_type', models.CharField(choices=[('single', 'Single'), ('double', 'Double')], max_length=10)),
                ('ac', models.BooleanField(choices=[(False, 'AC'), (True, 'Non-AC')])),
                ('balcony', models.BooleanField()),
                ('attached_bathroom', models.BooleanField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_management.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_management.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('single', 'Single'), ('double', 'Double')], max_length=10)),
                ('ac', models.BooleanField(choices=[(False, 'AC'), (True, 'Non-AC')])),
                ('balcony', models.BooleanField()),
                ('attached_bathroom', models.BooleanField()),
                ('status', models.SmallIntegerField(choices=[(-1, 'Pending'), (1, 'Approved'), (0, 'Rejected')], default=-1)),
                ('assigned_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='room_management.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
