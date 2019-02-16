"""playme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^developer/uploads/$', views.developer_uploads, name='developer_uploads'),
    url(r'^payment/success/$', views.payment_success, name='success'),
    url(r'^payment/cancel/$', views.payment_cancel, name='cancel'),
    url(r'^payment/error/$', views.payment_error, name='error'),
    url(r'^payment/(?P<game_id>[0-9]+)/$', views.payment, name='pay'),
    url(r'^play/(?P<game_id>[0-9]+)/$', views.play, name='play'),
    url(r'^(?P<game_id>[0-9]+)/$', views.buy, name='buy'),
    url(r'^test/edit/$', views.edit_upload, name='upload'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^mygames/$', views.mygames, name='mygames'),
    url(r'^$', views.home, name='home')

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
