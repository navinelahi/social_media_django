# Generated by Django 3.2.14 on 2022-07-11 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0014_comment_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
