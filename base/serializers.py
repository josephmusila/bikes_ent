from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models, services
from django.conf import settings
from .models import Rentals
from django.forms.models import model_to_dict


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField(validators=[

        UniqueValidator(
            queryset=models.User.objects.all(),
            message='A user with such email address already exists'
        )]
    )
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)
    location = serializers.CharField()
    account_type = serializers.CharField()

    class Meta:
        fields = ["id", "email", "location"]

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.UserDataClass(**data)

    def get_profile_picture_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(settings.MEDIA_URL + obj['avatar'])


class BikeSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all())

    class Meta:
        model = models.Bike
        fields = ("id","owner", "name", "description", "price", "image")
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['owner'] = UserSerializer(instance.owner).data
        return response

    # def validate(self, attrs):
    #     try:
    #         attrs["owner"]=models.User.objects.get(email=attrs['owner'])
    #         return attrs
    #     except models.User.DoesNotExist:
    #         raise serializers.ValidationError("User Does Not Exist")


class RentalSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all())
    owner = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all())
    bike = serializers.PrimaryKeyRelatedField(
        queryset=models.Bike.objects.all())

    class Meta:
        model = Rentals
        fields = ('id', "customer", "owner","bike", "date_of_renting",
                "date_of_return", "paid")
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bike'] = BikeSerializer(instance.bike).data
        response['client'] = UserSerializer(instance.customer).data
        return response

    def get_profile_picture_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(settings.MEDIA_URL + obj['bike_image'])


class RepairServiceSerializer(serializers.ModelSerializer):
    customer=serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    bike=serializers.PrimaryKeyRelatedField(queryset=models.Bike.objects.all())
    
    class Meta:
        model=models.RepairServices
        fields="__all__"
        depth=2

class PaymentServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.PaymentTransaction
        fields="__all__"
        depth=2