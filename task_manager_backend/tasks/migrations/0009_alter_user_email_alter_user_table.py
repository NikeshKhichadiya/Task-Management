# Generated by Django 5.1.7 on 2025-04-06 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
    ]
