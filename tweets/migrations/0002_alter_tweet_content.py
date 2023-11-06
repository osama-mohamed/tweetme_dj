# Generated by Django 4.2.7 on 2023-11-06 11:28

from django.db import migrations, models
import tweets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.CharField(blank=True, max_length=250, null=True, validators=[tweets.models.validate_content]),
        ),
    ]