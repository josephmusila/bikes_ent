from cProfile import label
import dataclasses
from . import models
from django.conf import settings
import jwt
from datetime import datetime
from datetime import timedelta
# import datetime

datetime.utcnow()
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .models import User,Bike


@dataclasses.dataclass

class UserDataClass:
    first_name: str
    last_name: str
    email: str
    phone: str
    avatar:str
    email: str
    account_type:str
    location:str
    password: str = None
    id: int=None
   

    @classmethod
    def from_instance(cls,user:"User")->"UserDataClass":
        return cls(first_name=user.first_name,last_name=user.last_name,email=user.email,phone=user.phone,id=user.id,avatar=user.avatar,location=user.location,account_type=user.account_type)

def create_user(user:"UserDataClass") ->"UserDataClass":
    instance=models.User(first_name=user.first_name,last_name=user.last_name,email=user.email,phone=user.phone,avatar=user.avatar,location=user.location,account_type=user.account_type)

    if user.password is not None:
        instance.set_password(user.password)

    instance.save()
    return UserDataClass.from_instance(instance)


def user_email_selector(email:str)->"User":
    user=models.User.objects.filter(email=email).first()

    return user
def create_token(user_id:int)->str:
    payload = dict(id=user_id, exp=datetime.utcnow() + timedelta(hours=24),iat=datetime.utcnow())

    
    token=jwt.encode(payload,settings.JWT_SECRET, algorithm="HS256")
    return token


class ImageService:
    id: int=None
    label:str
    image:str

    @classmethod
    def from_instance(cls,image:"models.ImagesForSlide")->"ImageService":
        return cls(id=image.id,label=image.label,image=image.image)

def create_image(image:"ImageService")->"ImageService":
    instance=models.ImagesForSlide(label=image.label,image=image.image)
    instance.save()
    return ImageService.from_instance(instance)

class BikeService:
    id: int = None
    owner:int
    price:str
    name:str
    description:str
    image:str

    # @classmethod
    # def __init__(self,name,owner):
    #     self.name=name
    #     self.owner=owner


    @classmethod
    def from_instance(cls,bike:"Bike")->"BikeService":
        return cls(id=bike.id,owner=bike.owner,name=bike.name,description=bike.description,image=bike.image)

def create_bike(bike:"BikeService")->"BikeService":
        instance=models.Bike(name=bike.name,description=bike.description,price=bike.price,owner=bike.owner,image=bike.image)
        instance.save()
        return BikeService.from_instance(instance)


