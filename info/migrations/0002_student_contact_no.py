# Generated by Django 5.0.6 on 2024-07-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='contact_No',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
