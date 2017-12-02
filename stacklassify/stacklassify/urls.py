"""stacklassify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.jobs,name="index"),
    path('classify/',views.jobs,name="jobs"),
    path('classify/record',views.record,name="record"),
    path('classify/reset', views.reset, name="reset"),
    path('scrape/stack',views.load_stack,name="scrape_stack"),
    path('scrape/remoteio', views.load_remoteio, name="scrape_remoteio"),
    path('person/add', views.add_person, name="add_person"),
]
