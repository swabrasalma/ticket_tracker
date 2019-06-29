from rest_framework import serializers
from api.models import Request, RequestComment, PerformedAction


class PutRequest(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('__all__')

class GetRequest(serializers.ModelSerializer):
    # attachments = serializers.SerializerMethodField()
    activity_log = serializers.SerializerMethodField()
    request_comments = serializers.SerializerMethodField()
    class Meta:
        model = Request
        fields = ('__all__')
    def get_attachments(self, req):
        try:
            return req.attachments
        except:
            return None
    def get_activity_log(self, req):
        pas = PerformedAction.objects.filter(affected_request = req.pk)
        pas = PutPerformedAction(pas, many=True)
        return pas.data
    def get_request_comments(self, req):
        rcs = RequestComment.objects.filter(request = req.pk)
        rcs = GetRequestComment(rcs, many=True)
        return rcs.data


class PutRequestComment(serializers.ModelSerializer):
    class Meta:
        model = RequestComment
        fields = ('__all__')


class GetRequestComment(serializers.ModelSerializer):
    class Meta:
        model = RequestComment
        fields = ('__all__')


class PutPerformedAction(serializers.ModelSerializer):
    class Meta:
        model = PerformedAction
        fields = ('__all__')


