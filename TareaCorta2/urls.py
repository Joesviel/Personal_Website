"""
URL configuration for TareaCorta2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from personal.views import blog_page_view, blog_post_view, add_comment_view

from personal.views import (
    land_page_view,
    blog_page_view,
    resume_page_view,
    about_me_page_view,
    blog_post_view,
    add_comment_view,
    subscribe_page_view,
    subscribe,
    home,
    logout_view,
    increment_favorites,
    increment_likes,
    delete_comment,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', land_page_view, name='landpage'),
    path('blog/', blog_page_view.as_view(), name='blogpage'),
    path('resume/', resume_page_view, name='resumepage'),
    path('aboutme/', about_me_page_view, name='aboutmepage'),
    path('blogpost/<int:pk>', blog_post_view.as_view(), name='blogpost'),
    path('blogpost/<int:pk>/comment', add_comment_view.as_view(), name='postcomment'),
    path('blogpost/<int:pk>/incrementfavorites/', increment_favorites, name='incrementfavorites'),
    path('blogpost/<int:pk>/incrementlikes/', increment_likes, name='incrementlikes'),
    path('blogpost/<int:pk>/deletecomment/', delete_comment, name='deletecomment'),
    path('subscribeblog/', subscribe_page_view, name='subscribeblog'),
    path('subscribe', subscribe, name='subscribe'),
    path('accounts/', include('allauth.urls')),
    path('googlelogin/', home, name='googlelogin'),
    path('logout', logout_view),

]
