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
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from backend import views
from playme.restapi import playviews



router = routers.DefaultRouter()
router.register(r'game', playviews.GameViewSet, base_name="games")
router.register(r'sales', playviews.TransactionViewSet, base_name="sales")
router.register(r'scores', playviews.ScoreViewSet, base_name="scores")




urlpatterns = [
    path('admin/', admin.site.urls),
    path('restapi/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^developer/dashboard/$', views.developer_dahsboard, name='developer_dashboard'),
    url(r'^payment/success/$', views.payment_success, name='success'),
    url(r'^payment/cancel/$', views.payment_cancel, name='cancel'),
    url(r'^payment/error/$', views.payment_error, name='error'),
    url(r'^payment/(?P<game_id>[0-9]+)/$', views.payment, name='pay'),
    url(r'^play/(?P<game_id>[0-9]+)/$', views.play, name='play'),
    url(r'^play/(?P<game_id>[0-9]+)/submit_score/$', views.submit_score, name='submit_score'),
    url(r'^play/(?P<game_id>[0-9]+)/save_game/$', views.save_game, name='save_game'),
    url(r'^play/(?P<game_id>[0-9]+)/load_game/$', views.load_game, name='load_game'),
    url(r'^search/', views.search, name='search'),
    url(r'^(?P<game_id>[0-9]+)/$', views.buy, name='buy'),
    url(r'^upload/delete/$', views.delete_upload, name='delete'),
    url(r'^upload/edit/$', views.edit_upload, name='edit'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^mygames/$', views.mygames, name='mygames'),
    url(r'^$', views.home, name='home'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^category/$', views.category, name='category'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate')

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
