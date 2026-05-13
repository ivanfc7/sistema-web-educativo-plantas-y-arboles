from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Planta
from ..serializer import PlantaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class PlantaVista(viewsets.ModelViewSet):
    queryset = Planta.objects.all()  
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Planta.objects.filter(usuario=self.request.user)
   
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(usuario=user)

    @action(detail=True, methods=['patch'], url_path='actualizar-etapa')
    def updateEtapa(self, request, pk=None):
        try:
            planta, created = Planta.objects.get_or_create(pk=pk, usuario=request.user)
        except Planta.DoesNotExist:
            return Response({"mensaje": "Planta no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        nueva_etapa = request.data.get("etapa")
        planta.etapa = nueva_etapa
        planta.save()
        return Response({"mensaje": "Etapa actualiza"}, status=status.HTTP_200_OK)