from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Q

from .. import models,serializers

class PaymentsDetailsView(generics.ListAPIView):
    serializer_class=serializers.PaymentServicesSerializer
    queryset=models.PaymentTransaction.objects.all()

    def get(self, request, *args, **kwargs):
        PaymentsDetailsView.queryset=models.PaymentTransaction.objects.filter(Q(bike=kwargs["bikeid"]))
        return super().get(request, *args, **kwargs)

    



