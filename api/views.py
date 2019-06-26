from django.shortcuts import render
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_jwt.utils import jwt_payload_handler

from api.serializers import PutRequest
from api import support_functions as SupportFunctions

from api.models import Request
import datetime, json


class RequestList(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    def post(self, request, format=None):
        authentication = SupportFunctions.get_authentication_details(request)
        print(request.data)
        # data = request.data.dict()
        print(data)

        response = {
            'status': 400,
            'message': 'Something went wrong on our side. Please try again'
        }
        return Response(response, status=status.HTTP_200_OK)


        rd = Request(
            requestor_name = data['requestor_name'].title(),
            phone_number = data['phone_number'],
            submission_comments = data['submission_comments'],
            attachments = request.FILES['attachments'],
            status = 'New',
            amount_paid_by_customer = data['amount_paid_by_customer'],
            payment_details = data['payment_details']
        )
        try:
            rd.save()
            response = {
                'status': 200,
                'message': 'The request has been added successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)




        
            

            




