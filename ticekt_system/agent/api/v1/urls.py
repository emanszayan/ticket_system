from django.urls import path
from .views import AuthTokenGenerator, LogOut, PasswordChangeView, change_user_password, UserListCreateAPIView, \
    UserRetrieveUpdateDestroyAPIView

app_name = 'agent'

urlpatterns = [
    # token
    path('login', AuthTokenGenerator.as_view(), name='auth-token'),
    # logout
    path('logout', LogOut.as_view(), name='logout'),
    # password
    path('password/change', PasswordChangeView.as_view(), name='password_change'),
    path('password/change/<int:pk>', change_user_password, name='change_user_password'),
    # user models
    path('users', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

]
