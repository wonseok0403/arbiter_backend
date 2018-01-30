from django.urls import path,include
from stockapi.api.views import (
    TickerAPIView,
    OHLCVAPIView,
    STOCKINFOAPIView,
    InfoAPIView,
    FinancialAPIView,
    FinancialRatioAPIView,
    QuarterFinacialAPIView,
    BuySellAPIView,
    )

app_name = 'stock-api'
urlpatterns = [
    path('ticker/', TickerAPIView.as_view(), name='ticker'),
    path('stockinfo/', STOCKINFOAPIView.as_view(), name='stockinfo'),
    path('ohlcv/', OHLCVAPIView.as_view(), name='ohlcv'),
    path('info/', InfoAPIView.as_view(), name='info'),
    path('financial/', FinancialAPIView.as_view(), name='financial'),
    path('financial-ratio/', FinancialRatioAPIView.as_view(), name='financial-ratio'),
    path('quarterfinacial/', QuarterFinacialAPIView.as_view(), name='quarterfinacial'),
    path('buysell/', BuySellAPIView.as_view(), name='buysell'),
]
