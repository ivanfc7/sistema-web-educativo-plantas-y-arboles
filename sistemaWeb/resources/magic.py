from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def generar_magic_token(email):
    return serializer.dumps(email, salt="magic-link")

def verify_magic_token(token, expiration=700):
    try:
        email = serializer.loads(token, salt="magic-link", max_age=expiration)
        return email
    except:
        return None
        raise