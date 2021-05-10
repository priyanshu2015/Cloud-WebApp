from .serializers import RootUserAuthCustomTokenSerializer, RootUserSerializer, RootUserRegisterSerializer, IAMUserRegisterSerializer, IAMUserSerializer
from rest_framework.views import APIView
from ..models import User, IAMUserAdditional, RootUserAdditional
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import parsers, renderers
from rest_framework.authentication import TokenAuthentication
from .permissions import IsRootUser
from rest_framework import serializers
import random

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

class IAMUserRegisterAPI(generics.GenericAPIView):
    serializer_class = IAMUserRegisterSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes =(IsAuthenticated, IsRootUser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        iam_user_email = serializer.validated_data['email']
        iam_user = serializer.save()
        iam_user.type = User.Types.IAM
        iam_user.save()
        key = generateIAMUserKey()
        try:
            iam_user_additional = IAMUserAdditional.objects.create(user = iam_user, root_user = request.user, key = key, iam_user_email = iam_user_email)
        except Exception as e:
            iam_user.delete()
            raise serializers.ValidationError({"result": [e]})
        return Response({
            "key":iam_user_additional.key,
            "result":["Account successfully created"]
            })


def generateIAMUserKey():
    key = random.randint(100000,999999)
    return key

class IAMUserLogin(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    )

    #renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        key = request.data.get("key")
        try:
            iam_user_additional = IAMUserAdditional.objects.get(key = key)
        except:
            raise serializers.ValidationError({"result":"user not found."})
        iam_user = iam_user_additional.user 
        token, created = Token.objects.get_or_create(user=iam_user)

        content = {
            'user': IAMUserSerializer(iam_user).data,
            'token': token.key,
        }

        return Response(content)