from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import RegisterView, VerifyEmail, LoginView, PasswordResetView, ConfirmPasswordResetView, NewPasswordView, LogoutView ,UpdateInformationView, DeleteAccountView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('confirm-password-reset/<uidb64>/<token>/', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
    path('new-password/', NewPasswordView.as_view(), name='new-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-information/', UpdateInformationView.as_view(), name='update-information'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]