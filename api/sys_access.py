from django.shortcuts import render
from django.contrib.auth import authenticate
from mtn_account_statement_issuance_backend import settings
from api.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.utils import jwt_payload_handler

from api import support_functions as SF
from django.db import transaction
import jwt, datetime


# Create your views here.
class UserRegistration(APIView):
    permission_classes = (AllowAny, )
    """
    Allows users to create accounts
    """
    def post(self, request, format=None):
        
        try:
            # open up a transaction to ensure 
            # we create the user, profile and account at once
            username = request.data['email'].lower()
            User.objects.create_user(
                username,
                username,
                request.data['password']
            )
            # get the newly created user object
            user = User.objects.get(
                username = username
            )
            user.first_name = request.data['f_name'].title()
            user.last_name = request.data['l_name'].title()
            user.country = request.data['country'].title()
            user.save()
            response = {
                "status": 200,
                "message": "A verification code has been sent to your email"
            }
            try:
                return Response(response, status=status.HTTP_200_OK)
            finally:
                EmailCommunication().send_account_verification_email(username)
    
        except:
            response = {
                "status": 400,
                "message": "Your account has not been created. Please make sure you provide valid details."
            }
            return Response(response, status=status.HTTP_200_OK)
       

class UserLogin(APIView):
    """
    Login of users
    """
    permission_classes = (AllowAny, )
    def post(self, request, format=None):
        
        # find if the user email exists in the platform db

        # send to external api for auth

        # generate token for the user

        # get the general details of the user
        try:
            username = request.data['username'].lower()
            password = 'password'
            mtn_login = SF.AdUser(username, password)
            is_mtn_staff = mtn_login.authenticate()

            if not is_mtn_staff:
                response = {
                    'code': 400,
                    'message': 'Invalid credentials'
                }
                return Response(response, status = status.HTTP_404_NOT_FOUND)

            user = authenticate(username = username, password = password)
            if user is not None:
                try:
                    auth_user = User.objects.get(username = username)                    
                    payload = jwt_payload_handler(auth_user)

                    response = {}   
                    
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    response['token'] = token
                    response['code'] = 200

                    return Response(response, status = status.HTTP_200_OK)

                except Exception as e:
                    print(str(e))
                    response = {}
                    response['message'] = str(e)
                    return Response(response, status = status.HTTP_400_BAD_REQUEST)
            else:
                response = {}
                response['message'] = 'Invalid credentials'
                return Response(response, status = status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            print(e)
            response = {}
            response['message'] = 'Please provide login credentials'
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_409_CONFLICT)
