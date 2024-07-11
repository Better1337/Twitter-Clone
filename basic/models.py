from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user}: {self.text} : {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User,auto_now=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    

    def __str__(self):
        return self.user.username

def user_did_save(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(user_did_save, sender=User)