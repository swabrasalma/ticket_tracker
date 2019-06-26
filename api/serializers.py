from rest_framework import serializers
from api.models import Request


class PutRequest(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('__all__')
