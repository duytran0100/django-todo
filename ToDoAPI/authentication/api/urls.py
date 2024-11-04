from django.urls import path
from authentication.api.views import CustomAuthToken


urlpatterns = [
    path('obtain-token/', CustomAuthToken.as_view())
]