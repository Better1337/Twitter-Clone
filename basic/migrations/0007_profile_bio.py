# Generated by Django 5.0.6 on 2024-07-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_tweet_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
    ]
