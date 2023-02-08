from django.shortcuts import render
from . import services,authentication
from . import serializers as user_serializer
from .models import User,Bike,Rentals,RepairServices
from rest_framework import views,response,exceptions,permissions,generics        
from django.db.models import Q   
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
# from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt

from .LipaNaMpesaOnline import sendSTK, check_payment_status
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .LipaNaMpesaOnline import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny

# Create your views here.


class LoginAPi(views.APIView):

    def post(self,request):

        email=request.data["email"]
        password=request.data["password"]
       
        user=services.user_email_selector(email=email)

        
        # cust=RegisterApi.post(self,request);

        if user is None:

            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(raw_password=password):

            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        queryset=User.objects.get(email=user)
        serializer=user_serializer.UserSerializer(queryset,context={"request":request})
        
        # info = RegisterApi.getData()
        token=services.create_token(user_id=user.id)
        resp=response.Response({"token":token,"user": serializer.data})
        resp.set_cookie(key="jwt",value=token,httponly=True)
        return resp

class RegisterApi(views.APIView):
    
    def post(self,request):


        serializer=user_serializer.UserSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)

        data=serializer.validated_data
        serializer.instance = services.create_user(user=data)
        print(data)


        # return response.Response(data=serializer.data)
        return response.Response({"message":"Account created Succesfully","user":serializer.data})


    def getData(request,self):
        info = self.post(self,request)
        return info

class AddBike(generics.ListAPIView):
    serializer_class=user_serializer.BikeSerializer
    allowed_methods=["POST","GET"]
    queryset=Bike.objects.all()

    def post(self,request):

        data=request.data
        serializer=self.serializer_class(data=data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(data['owner'])
        return response.Response(serializer.data)


    def get(self, request, *args, **kwargs):
        # print( kwargs['search'])
        # AddBike.queryset=Bike.objects.filter(Q(location__icontains=kwargs['search']))
        AddBike.queryset=Bike.objects.all()
                                                 
        
        return self.list(request={"request":request}, *args, **kwargs) 



    def getData(request,self):
        info = self.post(self,request)
        return info


class RentalsView(generics.ListAPIView):
    queryset=Rentals.objects.all()
    serializer_class=user_serializer.RentalSerializer
    allowed_methods=["POST","GET"]

   
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(data)
        return response.Response(serializer.data)


    def get(self, request, *args, **kwargs):
        print( kwargs['id'])
        RentalsView.queryset=Rentals.objects.filter(Q(customer__id=kwargs['id']))
        # RentalsView.queryset=Rentals.objects.all()
        # data=self.serializer_class(data=data)                                         
        
        return self.list(request={"request":request}, *args, **kwargs) 

    # def getData(request,self):
    #     info = self.post(self,request)
    #     return info

class RepairServicesView(views.APIView):
    serializer_class=user_serializer.RepairServiceSerializer
    queryset=RepairServices.objects.all()

    def post(self,request):
        data=request.data
        customer=data["customer"]
        bike=data["bike"]

        ownership=Bike.objects.filter(owner__id=customer)
        if len(ownership) == 0:
            return response.Response({"ownership_error":"Only the owner can ask for repair of this bike"})
        else:   
        
            serializer=user_serializer.RepairServiceSerializer(data=data,many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)


class SearchBike(generics.ListAPIView):
    serializer_class=user_serializer.BikeSerializer
    queryset=Bike.objects.all()
    # allowed_methods=["POST","GET"]

    def get(self, request, *args, **kwargs):
        SearchBike.queryset=Bike.objects.filter(Q(name__icontains=kwargs['search']) |
                                                Q(owner__location__icontains=kwargs["search"]) |
                                                Q(description__icontains=kwargs["search"])
        )
        return self.list(request, *args, **kwargs)

class GetLocations(views.APIView):
    

    def get():
        locations=[]
        


class PaymentTranactionView(ListCreateAPIView):
    def post(self, request):
        return HttpResponse("OK", status=200)


class SubmitView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        phone_number ="254" + str((data["phone"][1:]))
        print(phone_number)
        amount = float(data['amount'])
        print(amount)

        bike=data["bike"]

        entity_id = 0
        if data.get('entity_id'):
            entity_id = data.get('entity_id')

        paybill_account_number = None
        if data.get('paybill_account_number'):
            paybill_account_number = data.get('paybill_account_number')

        transaction_id = sendSTK(bike,phone_number, amount, entity_id, account_number=paybill_account_number)
        # b2c()
        message = {"status": "ok", "transaction_id": transaction_id}
        return Response(message, status=HTTP_200_OK)


class CheckTransactionOnline(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        transaction = PaymentTransaction.objects.filter(id=trans_id).get()
        try:
            if transaction.checkout_request_id:
                status_response = check_payment_status(transaction.checkout_request_id)
                return JsonResponse(
                    status_response, status=200)
            else:
                return JsonResponse({
                    "message": "Server Error. Transaction not found",
                    "status": False
                }, status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class CheckTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        trans_id = data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.is_finished,
                    "successful": transaction.is_successful
                },
                    status=200)
            else:
                # TODO : Edit order if no transaction is found
                return JsonResponse({
                    "message": "Error. Transaction not found",
                    "status": False
                },
                    status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class RetryTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction and transaction.is_successful:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.is_finished,
                    "successful": transaction.is_successful
                },
                    status=200)
            else:
                response = sendSTK(
                    phone_number=transaction.phone_number,
                    amount=transaction.amount,
                    orderId=transaction.order_id,
                    transaction_id=trans_id)
                return JsonResponse({
                    "message": "ok",
                    "transaction_id": response
                },
                    status=200)

        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Error. Transaction not found",
                "status": False
            },
                status=400)


class ConfirmView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
        request_data = json.dumps(request.data)
        request_data = json.loads(request_data)
        body = request_data.get('Body')
        resultcode = body.get('stkCallback').get('ResultCode')
        # Perform your processing here e.g. print it out...
        if resultcode == 0:
            print('Payment successful')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
            for data in metadata:
                if data.get('Name') == "MpesaReceiptNumber":
                    receipt_number = data.get('Value')
            transaction = PaymentTransaction.objects.get(
                checkout_request_id=requestId)
            if transaction:
                transaction.trans_id = receipt_number
                transaction.is_finished = True
                transaction.is_successful = True
                transaction.save()

        else:
            print('unsuccessfull')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            transaction = PaymentTransaction.objects.get(
                checkout_request_id=requestId)
            if transaction:
                transaction.is_finished = True
                transaction.is_successful = False
                transaction.save()

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1237867865"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)

    def get(self, request):
        return Response("Confirm callback", status=HTTP_200_OK)


class ValidateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
        request_data = request.data

        # Perform your processing here e.g. print it out...
        print("validate data" + request_data)

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1234567890"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)
