from django.urls import path

from posts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>.html', views.post, name='post'),
    path('<slug:slug>.html', views.post, name='page'),
]
