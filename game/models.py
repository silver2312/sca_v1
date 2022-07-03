from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Guild
class GuildList(models.Model):
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    exp = models.TextField(default=0)
    max_exp = models.TextField(default=100)
    time_create = models.DateTimeField(auto_now_add=True)
    
class GuildMember(models.Model):
    guild_id = models.ForeignKey(GuildList, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_guild = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    cong_hien = models.FloatField(default=0)
    time_join = models.DateTimeField(auto_now_add=True)