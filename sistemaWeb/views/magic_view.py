from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..resources.magic import generar_magic_token, verify_magic_token
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

@api_view(["POST"])
def magic_link(request):
    email = request.data.get("email")
    nombre = request.data.get("first_name")

    if not email:
        return Response( {"error": "Email requerido"}, status=status.HTTP_400_BAD_REQUEST )
    
    user, created = User.objects.get_or_create(
        username=email,
        defaults={"email": email, "first_name": nombre}
    )

    if not created and nombre:
        user.first_name = nombre
        user.save()

    token = generar_magic_token(email)
    link = f"http://127.0.0.1:5173/verify-magic/{token}"

    try:
        send_mail(
            "Verificar usuario",
            f"Ingresa a este link para verificar tu usuario y activar la cuenta: {link}",
            "ivanflores521111@gmail.com",
            [email],
        )
        print('enviando')
        return Response({"success": "Correo enviado"}, status=status.HTTP_200_OK)
    except:
        return Response({"error": "Correo no fue enviado"}, status=status.HTTP_400_BAD_REQUEST)
        raise

@api_view(["GET"])
def verify_magic(request):
    token = request.GET.get("token")
    email = verify_magic_token(token)

    if not email:
        return Response(
            {"error": "Token inválido o expirado"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Buscamos al usuario. 
    user, created = User.objects.get_or_create(
        username=email,
        defaults={"email": email}
    )

    refresh = RefreshToken.for_user(user)
    response = JsonResponse({
        "access": str(refresh.access_token),
        "is_new_user": created
    })

    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=False,  
        samesite="Lax",
        max_age=60 * 60 * 24 * 30
    )
    return response