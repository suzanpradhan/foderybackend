"""Fodery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from .decorator import check_token
from django.contrib.auth.decorators import login_required
from decorator_include import decorator_include


urlpatterns = [
    path('admin/',admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('general/', decorator_include(check_token,'General.urls')),
    path('general/', include('General.urls')),
    path('product/', include('Products.urls')),
    path('user/',include('CustomUser.urls')),
    path('settings/',include('Settings.urls')),
    path('order/',include('Order.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    path('dashboard/', include('Dashboard.modules.DashboardAuth.urls')),
    path('dashboard/',include('Dashboard.urls')),
    path('token/',check_token),
    path('quickOrder/',include('QuickOrder.urls'))

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# oleoleole = [{"path": 'general/', 'include': 'General.urls'}]

# for i in oleoleole:
#     urlpatterns += path(i['path'], decorator_include(check_token, include(i['include'])))