from django.contrib import admin
from django.conf import settings
from django.urls import include, path
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('api/', include('api.urls')),
    path('analysis/', include('analysis.urls')),
    path('', include('rankings.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
