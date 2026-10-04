from rest_framework import serializers

class SearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(max_length=100, allow_blank=False, trim_whitespace=True)
