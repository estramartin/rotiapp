import json
import logging
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class PagoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @action(detail=False, methods=['post'])
    def webhook(self, request):
        try:
            raw_data = request.body.decode('utf-8')
            logger.info(f'Raw webhook received: {raw_data}')

            # Intentar cargar el JSON malformado
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError as e:
                # Aquí puedes intentar corregir el JSON
                corrected_data = self.correct_json(raw_data)
                if corrected_data:
                    data = corrected_data
                else:
                    raise e

            logger.info(f'Corrected webhook received: {data}')
            return Response({'status': 'ok'})
        except json.JSONDecodeError as e:
            logger.error(f'JSON parse error: {e}')
            return Response({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return Response({'status': 'error', 'message': str(e)}, status=500)

    def correct_json(self, raw_data):
        # Intentar corregir el JSON
        try:
            # Ejemplo: Reemplazar comillas simples por comillas dobles
            corrected_data = raw_data.replace("'", '"')
            return json.loads(corrected_data)
        except json.JSONDecodeError:
            # Si no se puede corregir, retornar None
            return None
    