from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('creator/', admin.site.urls),
    path('',include('user.urls')),
    path('chat/', include('chat.urls')),
    path('b/', include('book.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
