# Generated by Django 4.2.4 on 2023-08-17 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_usermodel_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodel',
            options={'managed': True, 'ordering': ['-created_at', '-updated_at', '-id']},
        ),
    ]
