from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


api_urlpatterns = [
    path('', include('myApp.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
#For static file and media file
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


