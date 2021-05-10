from .serializers import RootUserAuthCustomTokenSerializer, RootUserSerializer, RootUserRegisterSerializer, IAMUserRegisterSerializer, IAMUserSerializer
from rest_framework.views import APIView
from ..models import User, IAMUserAdditional, RootUserAdditional, IAMUser, RootUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import parsers, renderers
from rest_framework.authentication import TokenAuthentication
from .permissions import IsRootUser
from rest_framework import serializers
import random
import uuid
from cloudproject import settings

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

import json
import os
class IAMUserRegisterAPI(generics.GenericAPIView):
    serializer_class = IAMUserRegisterSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes =(IsAuthenticated, IsRootUser)

    def post(self, request, *args, **kwargs):
        request.data['password'] = uuid.uuid4().hex
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        iam_user_email = serializer.validated_data['email']
        iam_user = serializer.save()
        iam_user.type = User.Types.IAM
        iam_user.save()
        plaintext = iam_user.username + serializer.validated_data['password']
        secretKey = settings.secretKey
        key = AESCipher(secretKey).encrypt(plaintext)
        #key = json.dumps(generateIAMUserKey(plaintext))
        #key = key.decode("utf-8")
        try:
            iam_user_additional = IAMUserAdditional.objects.create(user = iam_user, root_user = request.user, key = key, iam_user_email = iam_user_email)
        except Exception as e:
            iam_user.delete()
            raise serializers.ValidationError({"result": [e]})
        return Response({
            "key": plaintext,
            "result":["Account successfully created"]
            })




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
        username = key[0:32]
        
        # try:
        #     iam_user_additional = IAMUserAdditional.objects.get(key = key)
        # except:
        #     raise serializers.ValidationError({"result":"user not found."})

        try:
            iam_user = IAMUser.objects.get(username = username)
        except:
            raise serializers.ValidationError({"result":"User not found."})
        #iam_user = iam_user_additional.user 
        secretKey = settings.secretKey
        decrypted_key = AESCipher(secretKey).decrypt(iam_user.showAdditional.key)
        print("decryptedMsg", decrypted_key)
        if decrypted_key == key:
            token, created = Token.objects.get_or_create(user=iam_user)

            content = {
                'user': IAMUserSerializer(iam_user).data,
                'token': token.key,
            }

            return Response(content)
        else:
            raise serializers.ValidationError({"result":["Wrong Key"]})


import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]

