from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from certificates import views

def redirect_to_admin(request):
    return redirect('/admin/')


urlpatterns = [
    path('admin/certificates/generate/<int:certificate_id>/', views.generate_new),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path("admin/", admin.site.urls),
    path('', redirect_to_admin),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
