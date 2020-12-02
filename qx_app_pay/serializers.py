from rest_framework import serializers


class AppleSubscription(serializers.Serializer):

    b64_receipt = serializers.CharField(
        label="Base64 Apple Receipt")
