from django.conf import settings
from rest_framework import authentication,exceptions
import jwt
from rest_framework.authtoken.models import Token

from . import models

class CustomUserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        
        token = request.headers.get("Authorization")

        print(token)
        print("hello")

        if not token:
            return None
        try:
            payload=jwt.decode(token,settings.JWT_SECRET,algorithms=["HS256"])

        except:
            raise exceptions.AuthenticationFailed("Unauthorized Access")
        

        user=models.User.objects.filter(id=payload["id"]).first()

        return (user,None)


