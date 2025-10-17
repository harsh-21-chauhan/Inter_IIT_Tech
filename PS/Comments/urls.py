from django.contrib import admin
from django.urls import path,include
from Comments import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name ="home"),
    path('login/',views.loginUser,name='loginUser'),
    path('logout/',views.logoutUser,name='logoutUser'),
    path('post/<int:post_id>/',views.postDetail,name="postDetails"),
    path('tinymce/', include('tinymce.urls')),
    ] 
if settings.DEBUG:  # serve media files in dev only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)