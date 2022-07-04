from django.urls import path

from . import views
urlpatterns = [
    path('<str:host>/<int:host_id>/', views.home, name='book_home'),
    path('search/',views.search,name='book_search'),
    path('rate/',views.vote,name="book_vote"),
    path('de-cu/',views.de_cu,name="home_bk_de_cu"),
    path('chap/list/<int:bk_id>/', views.chapter_list, name="chapter_list"),
    path('check/all/<int:id>/',views.check_all,name="check-all-book"),
    path('<str:host>/<int:host_id>/<int:chap_id>/', views.data_chap, name='data_chap'),
    path('check-content/',views.check_content,name="check-content-book"),
]