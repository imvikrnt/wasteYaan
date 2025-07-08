import random, string, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
# from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer
from .utils.email_utils import send_user_registration_email
from .utils.captchaGenerator import generate_captcha_text
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenView(TokenRefreshView):
    """
    Handles refreshing the JWT access token using the refresh token.
    """
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Use the provided refresh token to generate a new access token
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            return Response({
                "access": new_access_token
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        print(data)
        required_fields = ['role', 'name', 'dob', 'gender', 'nationality', 'mobile', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(email=data['email']).exists():
            return Response({"error": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile=data['mobile']).exists():
            return Response({"error": "Mobile number is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(
                role=data['role'],
                name=data['name'],
                dob=data['dob'],
                gender=data['gender'],
                nationality=data['nationality'],
                mobile=data['mobile'],
                email=data['email'],
                password=make_password(data['password'])
            )
            print(user)
            user.user_id = user.generate_unique_id()
            user.save()

            try:
                send_user_registration_email(to_email=user.email, name=user.name, user_id=user.user_id)
            except Exception as e:
                print(f"Email sending failed: {e}")  # Optional: log properly

            return Response({
                "message": "User registered successfully",
                "user_id": user.user_id,
                "role": user.role,
                "name": user.name,
                "email": user.email
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"error": "Database error while creating user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get('role')
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        # Check if required fields are present
        if not user_id or not password:
            return Response({"error": "Both UserID and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # if User.objects.filter(email=data['email']).exists()
            # user = get_object_or_404(User, user_id=user_id)
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Check password validity
        if not check_password(password, user.password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            print("Login successful")
            print("Generated Refresh Token:", str(refresh))
            print("Generated Access Token:", access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token,
                'user': {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "user_id": user.user_id,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("Token generation error:", str(e))
            return Response({"error": "Token generation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
class UpdateProfileView(APIView):
    def put(self, request):
        print(request.data)
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update fields
        user.name = request.data.get('name', user.name)
        user.dob = request.data.get('dob', user.dob)
        user.gender = request.data.get('gender', user.gender)
        user.nationality = request.data.get('nationality', user.nationality)
        user.email = request.data.get('email', user.email)
        user.mobile = request.data.get('mobile', user.mobile)
        user.profile_img = request.data.get('profile_img', user.profile_img)

        # if request.FILES.get('profile_img'):
        #     user.profile_img = request.FILES.get('profile_img')

        user.save()
        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

# Store captcha temporarily
CAPTCHA_STORE = {}

class CaptchaAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        captcha_text = generate_captcha_text()
        CAPTCHA_STORE[key] = captcha_text

        return Response({
            "captcha_key": key,
            "captcha_text": captcha_text
        }, status=status.HTTP_200_OK)

class VerifyCaptchaAPIView(APIView):
    def post(self, request):
        captcha_key = request.data.get("captcha_key")
        captcha_input = request.data.get("captcha_input")

        if not captcha_key or not captcha_input:
            return Response({"error": "CAPTCHA required."}, status=status.HTTP_400_BAD_REQUEST)

        correct = CAPTCHA_STORE.get(captcha_key)
        if not correct or captcha_input.upper() != correct:
            return Response({"error": "Invalid CAPTCHA."}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: remove key after verification
        del CAPTCHA_STORE[captcha_key]

        return Response({"message": "CAPTCHA verified."}, status=status.HTTP_200_OK)

# In-memory OTP store
otp_store = {}

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

class ForgotPasswordView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        email = request.data.get("email")
        mobile = request.data.get("mobile")

        if not user_id or not email or not mobile:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, user_id=user_id)

            # Mobile number verification
            if not user.mobile:
                return Response({"error": "Mobile number not registered."}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.mobile != mobile:
                return Response({"error": "Mobile number does not match."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate OTP
            otp = generate_otp()
            expiry = timezone.now() + datetime.timedelta(seconds=180)

            otp_store[user.user_id] = {
                "otp": otp,
                "expiry": expiry
            }
            # Send OTP via email (add SMS sending here if needed)
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is {otp}. It is valid for 3 minutes.",
                from_email="esmshelpline@gmail.com",
                recipient_list=[user.email],
            )
            print(user.user_id,"send otp")
            return Response({"detail": "OTP sent to your email.", "user_id": user.user_id}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid User ID or Email."},status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        otp_entered = request.data.get("otp")
        print(request.data)
        otp_data = otp_store.get(user_id)
        try:
            user = get_object_or_404(User, user_id=user_id)
        except:
            return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not otp_data:
            return Response({"detail": "OTP not found. Please request again."}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > otp_data["expiry"]:
            return Response({"detail": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

        if otp_data["otp"] != otp_entered:
            print(user.user_id,"veriyotp")
            return Response({"detail": "Incorrect OTP.","user_id": user.user_id}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "OTP verified."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        new_password = request.data.get("new_password")
        password=make_password(new_password)
        
        if not user_id or not new_password:
            return Response({"detail": "User ID and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        print("Password reset request:", request.data)

        try:
            user = get_object_or_404(User, user_id=user_id)
            password=make_password(new_password)
            # Set the new password and save the user
            user.password = password
            # user.set_password(password)
            user.save()


            # After reset, remove OTP from memory if stored
            if user_id in otp_store:
                del otp_store[user_id]
            print(f"Password reset for user: {user.user_id}")

            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Generic error handling
            print("Error during password reset:", e)
            return Response({"detail": "An error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(APIView):
    def post(self, request):
        print(request.data)
        try:
            user_id = request.data.get('id')
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if not user_id or not old_password or not new_password:
                return Response({'error': 'Required fields are missing'}, status=status.HTTP_400_BAD_REQUEST)

            # user = User.objects.get(id=user_id)
            try:
            # if User.objects.filter(email=data['email']).exists()
            # user = get_object_or_404(User, user_id=user_id)
                user = User.objects.filter(id=user_id).first()
                if not user:
                    return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

            except:
                return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

            # Check password validity
            if not check_password(old_password, user.password):
              return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
            # Encrypt and update the password
            user.password = make_password(new_password)
            user.save()

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
