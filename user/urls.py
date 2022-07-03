from django.urls import path
from user.views import (
     ResetPasswordView, 
     UserBrowser, 
     ProfileBrowser,
     send_friend_request,
     list_friend_request,
     accept_friend_request,
     remove_friend,
     decline_friend_request,
     friends_list_view,)
from django.contrib.auth import views as auth_views
 
urlpatterns = [
     path('login/',auth_views.LoginView.as_view(next_page='/',template_name="auth/login.html"), name="login"),
     path('register/', UserBrowser.register, name='register'),
     path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
     path('', UserBrowser.home, name='home'),
     path('check-user/', UserBrowser.check_profile, name='check_profile'),
     path('forgot-password/', ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='auth/password/change_pwd.html'),
          name='password_reset_confirm'),
     path('password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name='auth/password/password_reset_complete.html'),
          name='password_reset_complete'),
     #profile
     path('menu-profile/', ProfileBrowser.menu_profile, name='menu_profile'),
     path('edit-profile/', ProfileBrowser.edit_profile, name='edit_profile'),
     path('profile/', ProfileBrowser.my_profile, name='my_profile'),
     path('profile/<int:user_id>/', ProfileBrowser.guest_profile, name='guest_profile'),
     path('profile/edit/', ProfileBrowser.edit_account, name='edit_account'),
     #friend
     path('friend/list/<int:user_id>/', friends_list_view, name='list'),
     path('friend/send/', send_friend_request, name='friend-request'),
     path('friend/list-request/', list_friend_request, name='list-friend-request'),
     path('friend/accept/<int:friend_request_id>/',accept_friend_request,name="accept-friend-request"),
     path('friend/remove/<int:receiver_user_id>/',remove_friend,name="remove-friend-request"),
     path('friend/decline/<int:friend_request_id>/',decline_friend_request,name="decline-friend-request"),
]