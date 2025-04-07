from django.urls import path
from .views import SignupAPIView, LoginAPIView, UserProfileAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user-profile/<int:user_id>/', UserProfileAPIView.as_view(), name='user_profile'),
]
