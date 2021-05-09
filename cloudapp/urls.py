from django.urls import path, include
from .api import api_views
urlpatterns = [
    path('api/rootuserlogin/', api_views.RootUserLogin.as_view(), name = "rootuserloginapi"),
    path('api/rootuserregister/', api_views.RootUserRegisterAPI.as_view(), name = "rootuserregisterapi"),
]