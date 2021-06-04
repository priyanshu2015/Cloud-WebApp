from django.urls import path, include
from .api import api_views
urlpatterns = [
    path('api/createvm/', api_views.CreateVirtualMachine.as_view(), name = "createvm"),
]