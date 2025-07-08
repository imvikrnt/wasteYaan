from django.urls import path
from .views import RegisterUserView, LoginView, UpdateProfileView, ForgotPasswordView,ChangePasswordView
from .views import CaptchaAPIView, VerifyCaptchaAPIView,VerifyOTPView,ResetPasswordView,RefreshTokenView
urlpatterns = [
    path('user/register/', RegisterUserView.as_view(), name='register'),
    path('user/login/', LoginView.as_view(), name='login/page'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user/update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('captcha/', CaptchaAPIView.as_view(), name='get-captcha'),
    path('captcha/verify/', VerifyCaptchaAPIView.as_view(), name='verify-captcha'),
    path('user/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('user/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('user/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('user/refresh-token/', RefreshTokenView.as_view(), name='token_refresh'),
]

# from django.urls import path
# from .views import RegisterUserView

# urlpatterns = [
#     path('register/', RegisterUserView.as_view(), name='register'),
# ]
