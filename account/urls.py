from django.urls import path
from .views import UserRegistrationView
from .views import UserLoginView
from .views import UserDataView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/', UserDataView.as_view(), name='user_data'),
]