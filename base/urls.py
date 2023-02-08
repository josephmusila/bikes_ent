from .  import views
from .premiums import premium_views
from django.urls import path

urlpatterns=[
    path("user/register",views.RegisterApi.as_view(),name="register"),
    path("user/login",views.LoginAPi.as_view(),name="login"),


    path("bikes/add",views.AddBike.as_view(),name="add_bike"),
    path("bikes/list",views.AddBike.as_view(),name="get_all"),


    path("rentals/new",views.RentalsView.as_view(),name="new_rentals"),
    path("rentals/history/<id>",views.RentalsView.as_view(),name="customer_rentals"),
    path("bikes/search/<search>",views.SearchBike.as_view(),name="search"),

    
    path("repairs",views.RepairServicesView.as_view(),name="repairs"),


     # register, confirmation, validation and callback urls
    path('transactions/<bikeid>',premium_views.PaymentsDetailsView.as_view(),name="myviews"),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path('confirm/', views.ConfirmView.as_view(), name='confirm'),
    path('check-online/', views.CheckTransactionOnline.as_view(), name='confirm-online'),
    path('check-transaction/', views.CheckTransaction.as_view(), name='check_transaction'),
]