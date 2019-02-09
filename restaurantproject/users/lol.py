from django.conf import settings
settings.configure()
from django.contrib.auth.models import User
user1 = User.objects.create_user(username="ognjen",password="djukic123")