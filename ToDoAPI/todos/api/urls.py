from django.urls import path, include
from todos.api.views import ToDoAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('todo', ToDoAPIViewSet, basename="todo")

urlpatterns = [
    path('', include(router.urls))
]