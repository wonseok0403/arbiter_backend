from django.urls import path,include
from stockapi.api.views import (
    TickerAPIView,
    OHLCVAPIView,
    STOCKINFOAPIView,
    InfoAPIView,
    )

app_name = 'stock-api'
urlpatterns = [
    path('ticker/', TickerAPIView.as_view(), name='ticker'),
    path('stockinfo/', STOCKINFOAPIView.as_view(), name='stockinfo'),
    path('ohlcv/', OHLCVAPIView.as_view(), name='ohlcv'),
    path('info/', InfoAPIView.as_view(), name='info')
]
