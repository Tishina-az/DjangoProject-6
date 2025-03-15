from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegisterView, CustomUserUpdate, email_verification

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:products_list'), name='logout'),
    path('user/update/<int:pk>/', CustomUserUpdate.as_view(), name='user_update'),
    path('confirm/<str:token>/', email_verification, name='confirm'),
]
