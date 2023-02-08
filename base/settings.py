from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'MPESA_CONFIG', None)

DEFAULTS = {
    'CONSUMER_KEY': 'BIi3nqVdy7yzEBEpk7NoAtFi5jXLGIND',
    'CONSUMER_SECRET': 'd1nTGGqaYYmF5ypG',
    'CERTIFICATE_FILE': None,
    'HOST_NAME': "http://127.0.0.1:8000/",
    'PASS_KEY': 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
    'SAFARICOM_API': 'https://sandbox.safaricom.co.ke',
    'AUTH_URL': '/oauth/v1/generate?grant_type=client_credentials',
    'SHORT_CODE': "174379",
    'TILL_NUMBER': None,
    'TRANSACTION_TYPE': 'CustomerBuyGoodsOnline',
}

api_settings = APISettings(USER_SETTINGS, DEFAULTS, None)
