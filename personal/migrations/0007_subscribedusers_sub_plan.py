# Generated by Django 5.0.6 on 2024-06-15 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0006_subscribedusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribedusers',
            name='sub_plan',
            field=models.CharField(default='Monthly', max_length=100),
            preserve_default=False,
        ),
    ]
