"""Air360 URL Configuration

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

from news import views
from users import user_views
from mailer import mailer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('login/', user_views.login_page, name="login"),
    path('register/', user_views.register_page, name="register"),
    path('logout/', user_views.logout_user, name="logout"),

    path('custom-results/', views.Custom_Results, name="custom-results"),
    path('custom-search/', views.Custom_Search, name="custom-search"),
    path('about/', views.about, name="about"),
    path('mail/', mailer_views.mail, name="mail"),
    path('mail-disable/', mailer_views.mail_disable, name="mail-disable"),
    # path('scheduled-mail/', mailer_views.scheduled_mail, name="scheduled-mail"),

]
