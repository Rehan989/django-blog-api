from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blogapi.urls')),
    path('user/', include('userauthapi.urls')),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


