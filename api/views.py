from django.shortcuts import render
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_jwt.utils import jwt_payload_handler

from api.serializers import PutRequest, GetRequest, PutRequestComment, PutPerformedAction
from api import support_functions as SupportFunctions

from api.models import User, Request, PerformedAction
import datetime, json

from django.views.decorators.csrf import csrf_exempt


class RequestList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        authentication = SupportFunctions.get_authentication_details(request)
        # data = request.data.dict()
        data = json.loads(request.body.decode('utf-8'))
        # print(data)

        rd = Request(
            project_with_issue=data['project_with_issue '],
            issue_title=data[' issue_title '],
            component_with_issue=data['component_with_issue'],
            description=data['description'],
            priority=data['priority'],
            assigned_to=data['  assigned_to '],
            status='Pending',
            added_by=User.objects.get(pk=authentication['user_id'])
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


class ActionPerformed:
    def __init__(self, request_id, user_id, action_performed):
        self.request_id = request_id
        self.user_id = user_id
        self.action_performed = action_performed

    def save(self):
        pa = PutPerformedAction(
            data = {
                'affected_request': self.request_id,
                'performed_by': self.user_id,
                'action': self.action_performed
            }
        )
        if pa.is_valid():
            pa.save()
            return True
        else:
            return False
    
    def determine_next_party(self):
        """
        Determines the next party to handle the request
        """
        user_roles = ['MFS_RECEPTION', 'QC_ADMIN', 'QC_MANAGER']
        # req_statuses = ['New', 'Reverted', 'Rejected', 'Approved']
        # get the request details
        print('request_id::::', self.request_id)
        


        req = Request.objects.get(pk = self.request_id)
        print(req.next_party)

        # if the current role is mfs reception and the 
        if req.status == 'New':
            req.next_party = user_roles[1]
            req.save()
            return True
        elif req.status == 'Reverted':
            # find the index of the current next_party and decrease
            current_party = user_roles.index(req.next_party)
            req.current_role = user_roles[int(current_party)-1]
            req.save()
            return True
        elif req.status == 'Approve' or req.status == 'Forward':
            # find the index of the current next_party and increase
            current_party = user_roles.index(req.next_party)
            req.current_role = user_roles[int(current_party)+1]
            req.save()
            return True
        else:
            return True


class HandleApprove:
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        authentication = SupportFunctions.get_authentication_details(request)
        # data = request.data.dict()
        data = json.loads(request.body.decode('utf-8'))
        token = data['request_action']
        comment = data['comment']
        request_id = data['id']
        requests = Request.objects.filter(id_iexact = request_id)
        if requests.exists():
            if token == 'approve':
                try:
                    rd._do_update()
                    response = {
                        'status': 200,
                        'message': 'The request has been approved successfully'
                    }
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    response = {
                        'status': 400,
                        'message': 'Something went wrong on our side. Please try again'
                    }
                    return Response(response, status=status.HTTP_200_OK)
            elif token == 'reject':
                try:
                    # rd._do_update()
                    response = {
                        'status': 200,
                        'message': 'The request has been rejected successfully'
                    }
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    response = {
                        'status': 400,
                        'message': 'Something went wrong on our side. Please try again'
                    }
                    return Response(response, status=status.HTTP_200_OK)
            elif token == 'delete':
                try:
                    # rd._do_update()
                    response = {
                        'status': 200,
                        'message': 'The request has been deleted successfully'
                    }
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    response = {
                        'status': 400,
                        'message': 'Something went wrong on our side. Please try again'
                    }
                    return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': 400,
                    'message': 'Unsupported request action. Please try again'
                }
                return Response(response, status=status.HTTP_200_OK)
