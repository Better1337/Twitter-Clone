# Generated by Django 5.0.6 on 2024-07-10 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_alter_tweet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
