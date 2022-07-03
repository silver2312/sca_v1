from django.contrib import admin
from user.models import Users, Profile, PathUser, FriendList, FriendRequest
from user.forms import UsersCreationFrom, ProfileUpdateForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UsersAdmin(UserAdmin):
    model = Users
    add_form = UsersCreationFrom

    list_display = (
        'id', 'email', 'name', 'email_verified_at', 'vip_time', 'level', 'profile_image', 'is_staff', 'is_superuser',
        'is_active')
    ordering = ('id', 'email', 'name', 'level')
    search_fields = ('email', 'name', 'level', 'id',)
    fieldsets = (
        (
            'User profile',
            {
                'fields': (
                    'name',
                    'email',
                    'email_verified_at',
                    'password',
                    'profile_image',
                    'level',
                    'vip_time',
                    'date_joined',
                    'last_login',
                )
            }
        ),
        (
            'User role',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                    'is_active',
                )
            }
        )
    )
    list_filter = ()
    add_fieldsets = (
                        None,
                        {
                            'fields': (
                                'email',
                                'name',
                                'password1',
                                'password2',
                            )
                        }
                    ),


class ProfileAdmin(admin.ModelAdmin):
    models = Profile
    add_form = ProfileUpdateForm
    list_display = (
        'id', 'background_image', 'name_music', 'url_music', 'des', 'game_lv', 'game_lv_percent', 'dong_te', 'ngan_te',
        'kim_te', 'm_e')
    ordering = ('id',)
    search_fields = ('id',)


class PathUserAdmin(admin.ModelAdmin):
    models = PathUser
    list_display = (
        'id', 'dang_doc', 'tu_truyen', 'log', 'game', 'tui_do', 'thanh_tuu', 'ky_nang',
        'tieu_phi','binh_luan',)
    ordering = ('id',)
    search_fields = ('id',)


admin.site.register(PathUser, PathUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Users, UsersAdmin)

#friend
class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user',]

    class Meta:
        model = FriendList


admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver',]
    search_fields = ['sender__name', 'receiver__name']

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)