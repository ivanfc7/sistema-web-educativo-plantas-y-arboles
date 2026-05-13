from rest_framework import viewsets
from ..models import AporteAmbiental
from ..serializer import AporteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class AporteVista(viewsets.ModelViewSet):
    serializer_class = AporteSerializer
    queryset = AporteAmbiental.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()
        plantaID = self.request.query_params.get('planta')
        if plantaID is not None:
            queryset = queryset.filter(planta = plantaID)
        return queryset
