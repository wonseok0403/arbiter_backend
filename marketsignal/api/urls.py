from django.urls import path,include
from marketsignal.api.views import (
    IndexAPIView,
    )

app_name = 'index-api'
urlpatterns = [
    path('index/', IndexAPIView.as_view(), name='index'),
]
