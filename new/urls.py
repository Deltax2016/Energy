from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api$', views.API , name='api'),
    url(r'^api/MINIGES$', views.MINIGES , name='miniges'),
    url(r'^api/VETROGEN$', views.VETROGEN , name='vetrogen'),
    url(r'^api/SOLNBAT$', views.SOLNBAT , name='solnbat'),
    url(r'^api/VIBOR$', views.VIBOR , name='vibor'),
    url(r'^form$', views.form , name='form'),

]