from django.urls import path
from .views import PlaceBetView, UserBetsView

urlpatterns = [
    path('place/', PlaceBetView.as_view(), name='place-bet'),
    path('my-bets/', UserBetsView.as_view(), name='user-bets'),
]