from django.urls import path
from .views import sign_up, login, get_user_data

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('login/', login, name='login'),
     path('user/<int:user_id>/', get_user_data, name='get_user_data'),
]