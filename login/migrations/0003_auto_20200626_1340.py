# Generated by Django 3.0.7 on 2020-06-26 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=42, unique=True),
        ),
    ]
