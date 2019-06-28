from rest_framework import serializers
from api.models import Request, RequestComment


class PutRequest(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('__all__')

class GetRequest(serializers.ModelSerializer):
    # attachments = serializers.SerializerMethodField()
    class Meta:
        model = Request
        fields = ('__all__')
    def get_attachments(self, req):
        try:
            return req.attachments
        except:
            return None


class PutRequestComment(serializers.ModelSerializer):
    class Meta:
        model = RequestComment
        fields = ('__all__')


class GetRequestComment(serializers.ModelSerializer):
    class Meta:
        model = RequestComment
        fields = ('__all__')


