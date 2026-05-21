from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status

class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        print(f"DEBUG: Cookie recibida: {refresh_token}")
        if refresh_token:
            request.data['refresh'] = refresh_token
        
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            print(f"ERROR REAL EN REFRESH: {e}")
            return Response({"error": str(e)}, status=401)