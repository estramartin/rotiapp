import logging
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class PagoViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def webhook(self, request):
        logger.info(f'Webhook received. {request.data}')
        return Response({'status': 'ok'})
    