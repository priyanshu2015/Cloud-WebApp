from .serializers import RootUserAuthCustomTokenSerializer, RootUserSerializer, RootUserRegisterSerializer
from rest_framework.views import APIView
from ..models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import parsers, renderers
from rest_framework.authentication import TokenAuthentication
from .permissions import IsRootUser

# Register API
class RootUserRegisterAPI(generics.GenericAPIView):
    serializer_class = RootUserRegisterSerializer
    authentication_classes=[]
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root_user = serializer.save()
        return Response({"result":["Account successfully created"]})


class RootUserLogin(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    )

    #renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = RootUserAuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'user': RootUserSerializer(user).data,
            'token': token.key,
        }

        return Response(content)

class IamUserRegisterAPI(generics.GenericAPIView):
    serializer_class = RootUserRegisterSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated, IsRootUser)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root_user = serializer.save()
        return Response({"result":["Account successfully created"]})
