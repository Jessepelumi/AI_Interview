from rest_framework import serializers

class RevokeGrantSerializer(serializers.Serializer):
    grant_id = serializers.IntegerField(min_value=1)

class CreateGrantSerializer(serializers.Serializer):
    document_id = serializers.UUIDField()
    principal_type = serializers.ChoiceField(choices=["membership", "group"])
    principal_id = serializers.CharField(max_length=80)
