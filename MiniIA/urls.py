"""MiniIA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from schedule_maker.views import process as s_process
from schedule_maker.views import upload as s_upload
from schedule_maker.views import reset_data as s_reset
from schedule_maker.views import home
from schedule_maker.views import download_file as s_download
from schedule_maker.views import grade_no_friends as s_no_friends
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('organized/<int:grade>', s_process, name="organized"),
    path('class/<int:grade>', s_upload, name="class"),
    path('missing_friends/<int:grade>', s_no_friends, name="grade_no_friends"),
    path('reset/<int:grade>', s_reset, name="reset data"),
    path('', home, name="homepage"),
    path('download/<int:grade>/<int:class_number>', s_download, name="download")
] + staticfiles_urlpatterns()
