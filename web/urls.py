from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/<path:long_url>', views.create, name='index'),
    path('get/<str:token>', views.get, name='index'),
    path('<str:token>', views.redirect_to, name='redirect'),
]