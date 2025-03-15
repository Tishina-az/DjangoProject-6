from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import RegisterView, CustomUserUpdate, email_verification, CustomLoginView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/update/<int:pk>/', CustomUserUpdate.as_view(), name='user_update'),
    path('confirm/<str:token>/', email_verification, name='confirm'),
]
