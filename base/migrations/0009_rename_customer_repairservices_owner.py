# Generated by Django 4.1.3 on 2022-12-02 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_repairservices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repairservices',
            old_name='customer',
            new_name='owner',
        ),
    ]
