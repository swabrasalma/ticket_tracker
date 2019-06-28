from django.shortcuts import render
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_jwt.utils import jwt_payload_handler

from api.serializers import PutRequest, GetRequest, PutRequestComment
from api import support_functions as SupportFunctions

from api.models import Request
import datetime, json

from django.views.decorators.csrf import csrf_exempt


class RequestList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        authentication = SupportFunctions.get_authentication_details(request)
        data = request.data.dict()
        # response = {
        #     'status': 200,
        #     'message': 'The request has been added successfully'
        # }
        # return Response(response, status=status.HTTP_200_OK)

        rd = Request(
            requestor_name = data['requestor_name'].title(),
            phone_number = data['phone_number'],
            submission_comments = data['submission_comments'],
            attachments = data['attachments'],
            status = 'New',
            amount_paid_by_customer = data['amount_paid_by_customer'],
            payment_details = data['payment_details'],
            added_by = authentication['user_id']
        )

        # data = request.data
        # # data['status'] = 'NEW'
        # r_ser = PutRequest(data=request.data)
        # if r_ser.is_valid():
        #     r_ser.save()
        #     rd

        #     response = {
        #         'status': 200,
        #         'message': 'The request has been added successfully'
        #     }
        #     return Response(response, status=status.HTTP_200_OK)
        # else:
        #     print(r_ser.errors)
        #     response = {
        #         'status': 400,
        #         'message': 'Something went wrong on our side. Please try again'
        #     }
        #     return Response(response, status=status.HTTP_200_OK)

        
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

    def get(self, request, format=None):
        requests = Request.objects.all()
        requests = GetRequest(requests, many=True)
        return Response(requests.data, status = status.HTTP_200_OK)


class RequestComment(APIView):
    def post(self, request, format=None):
        authentication = SupportFunctions.get_authentication_details(request)
        post_data = {
            'request': request.data['request'],
            'comment': request.data['comments'],
            'user': authentication['user_id']    
        }           
        
        rc = PutRequestComment(data = post_data)
        if rc.is_valid():
            rc.save()
            try:
                response = {
                    'status': 200,
                    'message': 'Your action has been performed successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            finally:
                rq = Request.objects.get(pk=request.data['request'])
                rq.status = request.data['action']
                rq.save()
                if request.data['action'] == 'Approve':
                    # send out notifications
                    pass
                
        else:
            print(rc.errors)
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)


            




