from django.urls import path, include
from .api import api_views
urlpatterns = [
    path('api/rootuserlogin/', api_views.RootUserLogin.as_view(), name = "rootuserloginapi"),
    path('api/rootuserregister/', api_views.RootUserRegisterAPI.as_view(), name = "rootuserregisterapi"),
    path('api/iamuserregister/', api_views.IAMUserRegisterAPI.as_view(), name = "iamuserregisterapi"),
    path('api/iamuserlogin/', api_views.IAMUserLogin.as_view(), name = "iamuserloginapi"),
    path('api/listpermissions/', api_views.ListPermissions.as_view(), name = "listpermissions"),
]