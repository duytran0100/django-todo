from django.urls import include, path

urlpatterns = [
    path("", include("todos.api.urls")),
    path("auth/", include("authentication.api.urls")),
]
