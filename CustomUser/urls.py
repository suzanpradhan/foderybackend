from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views
from CustomUser.models import Address
from CustomUser.utils import refresh_token_view
from django.contrib.auth import views as auth_views

from CustomUser.views import AddressUpDelView, AddressView, CallbackFacebookSignin, ChangeDefault, DeactivateAccount, DeliveryLogin, ForgetPasswordBeta, ForgotPassword,GetUserAddress, GetUser, GetUserProfile, Login, PasswordEmpty, RedirectFacebookSignin, ReferMe, Register, ReviewHistory, SetPw, TestVerifyUserPhone, UpdateProfile, VerifyOTPCode, VerifyUserPhone, activation,UpdateUserPw, referCheck, smtpChangePw, token_validity, RedirectGoogleSignin, CallbackGoogleSignin, CheckPhoneVerification, password_reset_request, password_reset_confirm

urlpatterns = [
    path('obtain-token/', views.obtain_auth_token),
    path('validate_token/', token_validity),
    path('login/',Login.as_view()),
    path('deliverylogin/',DeliveryLogin.as_view()),
    # path('googleLogin/',GoogleLogin.as_view()),
    path('getNewAccess/',refresh_token_view),
    path('register/',Register.as_view()),
    path('activate/', activation),
    path('updateProfile/', UpdateProfile.as_view()),
    path('getUserProfile/', GetUserProfile.as_view()),
    path('updatePassword/', UpdateUserPw.as_view()),
    path('changePassword/<str:token>/', ForgotPassword.as_view()),
    path('changePassword/', ForgotPassword.as_view()),
    path('refercode/', referCheck.as_view()),
    path('refer_me/', ReferMe.as_view()),
    path('passwordEmpty/', PasswordEmpty.as_view()),
    path('setPassword/', SetPw.as_view()),
    path('forgot_password', ForgetPasswordBeta.as_view()),
    path('addAddress/', AddressView.as_view()),
    path('updateDeleteAddress/<int:id>/', AddressUpDelView.as_view()),
    path('setDefaultAddress/<int:id>/', ChangeDefault.as_view()),
    path('get_user/',GetUser.as_view()),
    path('get_user_address/',GetUserAddress.as_view()),
    path('google/signin', RedirectGoogleSignin),
    path('google/callback/', CallbackGoogleSignin),
    path('facebook/signin', RedirectFacebookSignin),
    path('facebook/callback/', CallbackFacebookSignin),
    path('check_phone_verification', CheckPhoneVerification.as_view()),
    path('verify_phone', VerifyUserPhone.as_view()),
    path('verify_code', VerifyOTPCode.as_view()),
    path('test_verify_phone', TestVerifyUserPhone.as_view()),
    path('deactivate_account', DeactivateAccount.as_view()),
    path('review_history', ReviewHistory.as_view()),
    # path('smtp/',smtp.as_view()),

    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),     
]   