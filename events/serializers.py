from rest_framework import serializers
from .models import TransferEvent


class TransferEventSerializer(serializers.ModelSerializer):
    """
    Serializer for the TransferEvent model, mapping the model fields to JSON.
    """
    class Meta:
        model = TransferEvent
        fields = ['token_id', 'from_address', 'to_address', 'transaction_hash', 'block_number']
