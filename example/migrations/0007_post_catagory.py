# Generated by Django 2.1 on 2018-10-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='catagory',
            field=models.CharField(default='abc', max_length=50),
        ),
    ]
