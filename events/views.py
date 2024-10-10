from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TransferEvent
from .serializers import TransferEventSerializer


@api_view(['GET'])
def token_transfer_history(request, token_id):
    """
    API view to retrieve the transfer history of a given token by its token ID.
    """
    events = TransferEvent.objects.filter(token_id=token_id)
    if events.exists():
        serializer = TransferEventSerializer(events, many=True)
        return Response(serializer.data)

    return Response(
        {'message': 'No events found for this token ID'}, status=404
    )
