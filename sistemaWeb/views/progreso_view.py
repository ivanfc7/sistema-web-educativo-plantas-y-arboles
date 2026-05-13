from datetime import date
from rest_framework import viewsets
from ..models import ProgresoJuego
from ..serializer import ProgresoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProgresoVista(viewsets.ModelViewSet):
    serializer_class = ProgresoSerializer
    queryset = ProgresoJuego.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return ProgresoJuego.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(usuario=user)

    @action(detail=False, methods=['post'], url_path='incrementar-contador-msj')
    def incrementarContadorMensaje(self, request):
        progreso, created = ProgresoJuego.objects.get_or_create(usuario=request.user)
        progreso.cantidadMsjDesbloqueados += 1
        progreso.save()
        return Response({"mensaje":"Item mensaje desbloqueado", "cantidad": progreso.cantidadMsjDesbloqueados}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'], url_path='incrementar-contador-apzj')
    def incrementarContadorAprendizaje(self, request):
        progreso, created = ProgresoJuego.objects.get_or_create(usuario=request.user)
        progreso.cantidadApzjDesbloqueados += 1
        progreso.save()
        return Response({"mensaje":"Item aprendizaje desbloqueado", "cantidad":progreso.cantidadApzjDesbloqueados}, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['get'], url_path='puede-jugar')
    def puedeJugar(self, request):
        progreso, created = ProgresoJuego.objects.get_or_create(usuario=request.user)

        hoy = date.today()
        if progreso.fechaJuego == hoy:
            return Response({"habilitado": False, "mensaje": "Ya jugaste hoy"}, status=status.HTTP_200_OK)
        
        return Response({"habilitado": True, "mensaje": "Juega el reto diario"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='actualizar-fecha')
    def updateFechaJuego(self, request):
        progreso, created = ProgresoJuego.objects.get_or_create(usuario=request.user)
        progreso.fechaJuego = date.today()
        progreso.save()
        return Response({"mensaje":"Se actualizo la fecha del juego"}, status=status.HTTP_200_OK)