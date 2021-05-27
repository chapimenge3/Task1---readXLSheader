from rest_framework import serializers


class ExcelSerializer(serializers.Serializer):
    file = serializers.CharField()
    row = serializers.IntegerField(required=False, default=1)

class ExcelAnalaysisSerializer(serializers.Serializer):
    file = serializers.CharField()
    row = serializers.IntegerField(required=False, default=1)
    row_number = serializers.IntegerField()