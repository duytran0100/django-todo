"""
URL configuration for ToDoAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ToDo API",
        default_version="v1",
        description="A simple ToDo API",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="API License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=os.environ.get("BASE_URL"),
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path('admin/', admin.site.urls),
    path("v1/", include("ToDoAPI.api")),
]

handler500 = "rest_framework.exceptions.server_error"