import os
from django.db import models
from django.conf import settings
from game.models import GuildList
from django.template.defaultfilters import slugify
# Create your models here.
def delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)
       
class Room(models.Model):
    name = models.CharField(max_length=255,null=False,unique=True)
    slug = models.CharField(null=True,unique=True,max_length=255)
    guild_id = models.OneToOneField(GuildList,models.SET_NULL,blank=True,null=True,related_name="room_guild_id")
    public = models.BooleanField(default=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True,null=True, related_name="room_sender")
    revicer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True,null=True, related_name="room_reciever")
    mod = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True,null=True,  related_name="mod_chat")
    banners = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True,null=True,  related_name="chat_ban")
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name, ok='_', only_ascii=True)
        super(Room,self).save(*args, **kwargs)
    #add
    def add_guild_room(self, guild_id):
        self.guild_id.add(guild_id)
        self.save()
    def add_room_mod(self, user):
        self.mod.add(user)
        self.save()
    def add_room_ban(self, user):
        self.banners.add(user)
        self.save()
    #remove
    def remove_mod(self, user):
        if user in self.mod.all():
            self.mod.remove(user)
            self.save()
    def remove_ban(self, user):
        if user in self.banners.all():
            self.banners.remove(user)
            self.save()
            
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='room_messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

class Emote(models.Model):
    text = models.CharField(max_length=30,null=False,unique=True)
    img = models.ImageField(upload_to='static/img/icons/emotes/',null=False)
    
def bbcode(text):
    return text