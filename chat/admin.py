from django.contrib import admin
from .models import Room, Message
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    models = Room
    list_display = (
        'id', 'name', 'slug', 'guild_id', 'mod', 'banners')
    ordering = ('id','name',)
    search_fields = ('id', 'guild_id', 'mod', 'banners',)
    prepopulated_fields = {"slug": ("name",)}
    
class MessageAdmin(admin.ModelAdmin):
    models = Message
    list_display = ('id', 'room', 'user', 'content', 'date_added')
    search_fields = ('id', 'room', 'user', )
                     
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)