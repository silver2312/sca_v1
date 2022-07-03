from django.contrib import admin
from .models import TheLoai, Tag, Book, Rating
# Register your models here.

class TheLoaiAdmin(admin.ModelAdmin):
    models = TheLoai
    list_display = (
        'id', 'name', 'des')
    ordering = ('id',)
    search_fields = ('id',)
admin.site.register(TheLoai, TheLoaiAdmin)
    
class TagAdmin(admin.ModelAdmin):
    models = Tag
    list_display = (
        'id', 'name', 'des')
    ordering = ('id',)
    search_fields = ('id',)
admin.site.register(Tag, TagAdmin)

class BookAdmin(admin.ModelAdmin):
    models = Book
    list_display = (
        'id','image' ,'url' ,'title', 'author', 'user', 'des', 'show_cate','show_tag', 'chapter', 'comment', 'name_bk', 'trang_thai', 'de_cu', 'date_add', 'date_update')
    ordering = ('id',)
    search_fields = ('id',)
    def show_cate(self, obj):
        return " - ".join([a.name for a in obj.the_loai.all()])
    def show_tag(self, obj):
        return " - ".join([a.name for a in obj.tag.all()])
admin.site.register(Book, BookAdmin)

class RatingAdmin(admin.ModelAdmin):
    models = Rating
    list_display = (
        'id', 'user', 'book', 'rating')
    ordering = ('id',)
    search_fields = ('id',)
admin.site.register(Rating, RatingAdmin)
